#include <stdio.h>
#include <string.h>
#define MAXL 512

char line1[MAXL], line2[MAXL];


int main() {
  FILE *ps = fopen("Proteins.fa", "r");
  FILE *ss = fopen("SSpro.dssp", "r");
  FILE *ds = fopen("dataset.txt", "w");
  
  int i, j, e;
  
  e = i = j = 0;
  while (fgets(line1, MAXL, ps)) {
    fgets(line2, MAXL, ss);
    
    if(i) {
      fprintf(ds, "%s", line1);
      fprintf(ds, "%s", line2);
    } else {
      if (strcmp(line1, line2)) {
	e++;
      }
      fprintf(ds, "%s", line1);
    }
    
    i = !i;
    
    j++;
  }
  
  fclose(ps);
  fclose(ss);
  fclose(ds);
  
  printf("errors: %d, total: %d\n", e, j);
  
  return 0;
}