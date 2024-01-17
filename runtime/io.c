#include <stdio.h>
#include <stdint.h>

int64_t input_int64_t() {
  int64_t x;
  scanf("%ld", &x);
  return x;
}

void output_int64_t(int64_t x) {
  printf("%ld\n", x);
}
