#include <stdio.h>
#include <stddef.h>


extern int vetor[];
extern const size_t vetor_len;

void swap(int * v, int i, int n){
    int aux = v[i];
    
    v[i] = v[n];
    v[n] = aux;
}

int particiona(int * v, int low, int high){
    int j = low - 1;  //quantidade de nodos maiores que v[high] que e o pivo
    int end = high;
    for (int i = low; i <= high; i++) {
        if(v[i] < v[high]){
            j++;    //quantidade de nodos menores que j aumenta 1
            swap(v, j, i); //substitui pelo ultimo 
        }
    }
    
    swap(v, j+1, high);
    
    return j+1;
}


void quick_sort(int * v, int low, int high){
    int i;
    
    if(low >= high) return;
    
    i = particiona(v, low, high);
 
        
    quick_sort(v, low, i-1);
    quick_sort(v, i+1, high); 
}

int main ( void ) {

    int n;
    
    n = vetor_len;

    quick_sort(vetor, 0, n-1);
    
    /*for (int i = 0; i < n; i++)
        printf("%d ", vetor[i]);
    */

    return 0;
}
