#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "traffic.h"

extern struct intersection isection;

/**
 * Populate the car lists by parsing a file where each line has
 * the following structure:
 *
 * <id> <in_direction> <out_direction>
 *
 * Each car is added to the list that corresponds with 
 * its in_direction
 * 
 * Note: this also updates 'inc' on each of the lanes
 */
void parse_schedule(char *file_name) {
    int id;
    struct car *cur_car;
    struct lane *cur_lane;
    enum direction in_dir, out_dir;
    FILE *f = fopen(file_name, "r");

    /* parse file */
    while (fscanf(f, "%d %d %d", &id, (int*)&in_dir, (int*)&out_dir) == 3) {

        /* construct car */
        cur_car = malloc(sizeof(struct car));
        cur_car->id = id;
        cur_car->in_dir = in_dir;
        cur_car->out_dir = out_dir;

        /* append new car to head of corresponding list */
        cur_lane = &isection.lanes[in_dir];
        cur_car->next = cur_lane->in_cars;
        cur_lane->in_cars = cur_car;
        cur_lane->inc++;
    }

    fclose(f);
}

/**
 * TODO: Fill in this function
 *
 * Do all of the work required to prepare the intersection
 * before any cars start coming
 * 
 */
void init_intersection() {
    int i;
    for (i = 0; i < 4; i++) {
        pthread_mutex_init(&(isection.quad[i]), NULL);

        pthread_mutex_init(&(isection.lanes[i].lock), NULL);
        pthread_cond_init(&(isection.lanes[i].producer_cv), NULL);
        pthread_cond_init(&(isection.lanes[i].consumer_cv), NULL);
        isection.lanes[i].in_cars = NULL;
        isection.lanes[i].out_cars = NULL;
        isection.lanes[i].inc = 0;
        isection.lanes[i].passed = 0;
        isection.lanes[i].buffer = malloc(LANE_LENGTH * sizeof(struct car *));
        isection.lanes[i].head = 0;
        isection.lanes[i].tail = 0;
        isection.lanes[i].capacity = LANE_LENGTH;
        isection.lanes[i].in_buf = 0;
    }

}

/**
 * TODO: Fill in this function
 *
 * Populates the corresponding lane with cars as room becomes
 * available. Ensure to notify the cross thread as new cars are
 * added to the lane.
 * 
 */
void *car_arrive(void *arg) {
    struct lane *l = arg;

    while(l->in_cars != NULL && l->inc != 0){
        pthread_mutex_lock(&(l->lock));
        //if the lane is full of cars and no more car come in, wait
        while(l->in_buf == l->capacity){
            pthread_cond_wait(&(l->producer_cv), &(l->lock));
        }

        l->buffer[l->tail] = l->in_cars;
        l->tail = (l->tail + 1) % (l->capacity); //back to the front
        l->in_cars = (l->in_cars)->next;

        l->inc--;
        l->in_buf++;

        pthread_cond_signal(&(l->consumer_cv));
        pthread_mutex_unlock(&(l->lock));
    }

    return NULL;
}

/**
 * TODO: Fill in this function
 *
 * Moves cars from a single lane across the intersection. Cars
 * crossing the intersection must abide the rules of the road
 * and cross along the correct path. Ensure to notify the
 * arrival thread as room becomes available in the lane.
 *
 * Note: After crossing the intersection the car should be added
 * to the out_cars list of the lane that corresponds to the car's
 * out_dir. Do not free the cars!
 *
 * 
 * Note: For testing purposes, each car which gets to cross the 
 * intersection should print the following three numbers on a 
 * new line, separated by spaces:
 *  - the car's 'in' direction, 'out' direction, and id.
 * 
 * You may add other print statements, but in the end, please 
 * make sure to clear any prints other than the one specified above, 
 * before submitting your final code. 
 */
void *car_cross(void *arg) {
    struct lane *l = arg;
    struct lane *nl;

    while(l->in_buf != 0 || l-> in_cars != NULL){
        pthread_mutex_lock(&(l->lock));
        //if the lane empty and no cars waiting to cross, wait
        if(l->in_buf == 0){
            pthread_cond_wait(&(l->consumer_cv), &(l->lock));
        }

        struct car *cur = l->buffer[l->head];
        printf("%d %d %d\n", cur->in_dir, cur->out_dir, cur->id);
        int *path = compute_path(cur->in_dir, cur->out_dir);
        int i;
        for(i = 0; i < 4; i++){
            if (path[i] != 0){
                pthread_mutex_lock(&(isection.quad[path[i] - 1]));
            }
        }
        nl = &isection.lanes[cur->out_dir];
        cur->next = nl->out_cars;
        nl->out_cars = cur;
        l->head = (l->head + 1) % (l->capacity); //back to the front
        l->passed++;
        l->in_buf--;

        for(i = 0; i < 4; i++){
            if (path[i] != 0){
                pthread_mutex_unlock(&(isection.quad[path[i] - 1]));            
            }
        }
        pthread_cond_signal(&(l->producer_cv));
        pthread_mutex_unlock(&(l->lock));

    }
    return NULL;
}

void generate_path(int *path, int q1, int q2, int q3, int q4) {
    path[0] = q1;
    path[1] = q2;
    path[2] = q3;
    path[3] = q4;
}

/**
 * TODO: Fill in this function
 *
 * Given a car's in_dir and out_dir return a sorted 
 * list of the quadrants the car will pass through.
 * 
 */
int *compute_path(enum direction in_dir, enum direction out_dir) {
    int route[4] = {0};

    if(in_dir == NORTH){
        if(out_dir == NORTH){
            generate_path(route, 1, 2, 3, 4);
        }else if(out_dir == SOUTH){
            generate_path(route, 2, 3, 0, 0);
        }else if(out_dir == WEST){
            generate_path(route, 2, 0, 0, 0);
        }else if(out_dir == EAST){
            generate_path(route, 2, 3, 4, 0);
        }
    }else if(in_dir == SOUTH){
        if(out_dir == NORTH){
            generate_path(route, 1, 4, 0, 0);
        }else if(out_dir == SOUTH){
            generate_path(route, 1, 2, 3, 4);
        }else if(out_dir == WEST){
            generate_path(route, 1, 2, 4, 0);
        }else if(out_dir == EAST){
            generate_path(route, 4, 0, 0, 0);
        }

    }else if(in_dir == WEST){
        if(out_dir == NORTH){
            generate_path(route, 1, 3, 4, 0);
        }else if(out_dir == SOUTH){
            generate_path(route, 3, 0, 0, 0);
        }else if(out_dir == WEST){
            generate_path(route, 1, 2, 3, 4);
        }else if(out_dir == EAST){
            generate_path(route, 3, 4, 0, 0);
        }
    }else if(in_dir == EAST){
        if(out_dir == NORTH){
            generate_path(route, 1, 0, 0, 0);
        }else if(out_dir == SOUTH){
            generate_path(route, 1, 2, 3, 0);
        }else if(out_dir == WEST){
            generate_path(route, 1, 2, 0, 0);
        }else if(out_dir == EAST){
            generate_path(route, 1, 2, 3, 4);
        }
    }
    return NULL;
}