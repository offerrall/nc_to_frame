#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>
#include <ctype.h>

void update_bbox_from_line(const char* line,
                           double* min_x,
                           double* max_x,
                           double* min_y,
                           double* max_y) {

    const char* p = line;
    while (*p) {
        if (*p == 'X' || *p == 'Y') {
            char axis = *p++;
            char buf[64];
            int i = 0;
            while (*p && (isdigit(*p) || *p == '.' || *p == '-' || *p == '+') && i < 63) {
                buf[i++] = *p++;
            }
            buf[i] = '\0';
            double val = atof(buf);
            if (axis == 'X') {
                if (val < *min_x) *min_x = val;
                if (val > *max_x) *max_x = val;
            } else {
                if (val < *min_y) *min_y = val;
                if (val > *max_y) *max_y = val;
            }
        } else {
            p++;
        }
    }
}

void get_bounding_box(const char* file_path,
                      double* min_x,
                      double* max_x,
                      double* min_y,
                      double* max_y) {

    *min_x = DBL_MAX;
    *max_x = -DBL_MAX;
    *min_y = DBL_MAX;
    *max_y = -DBL_MAX;

    FILE* file = fopen(file_path, "r");
    if (!file) {
        fprintf(stderr, "Error opening file: %s\n", file_path);
        return;
    }

    char line[512];
    while (fgets(line, sizeof(line), file)) {
        update_bbox_from_line(line, min_x, max_x, min_y, max_y);
    }

    fclose(file);
}