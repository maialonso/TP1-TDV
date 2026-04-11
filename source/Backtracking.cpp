#include "Backtracking.h"
#include <limits>


// función recursiva
void encontrarSeamBacktrackingRec(const std::vector<std::vector<double>>& energia, int i,int j,int n ,int m ,std::pair<std::vector<int>, double>&S ,std::pair<std::vector<int>, double>&B) {
    if(i==n){                                           // caso base: es el final de la imagen
        if(B.first.empty() || S.second < B.second){     // si encontró un camino mejor actualiza y guarda ese camino
            B=S;
        }
        return;
    }

    if (S.second < B.second) {              // poda: solo sigue si el camino actual es mejor que el mejor conocido
        
        if(j>0){                            // baja por la izquierda siempre y cuando no esté en un borde
            S.first.push_back(j - 1);
            S.second+=energia[i][j-1];
            encontrarSeamBacktrackingRec(energia, i + 1, j - 1, n, m, S, B);
            S.second-=energia[i][j-1];
            S.first.pop_back();
        }

        S.first.push_back(j);               // en todos los casos baja por la rama del medio
        S.second+=energia[i][j];
        encontrarSeamBacktrackingRec(energia, i + 1, j, n, m, S, B);
        S.second-=energia[i][j];
        S.first.pop_back();

        if(j<m-1){                          // baja por la rama derecha siempre y cuando no esté en un borde
            S.first.push_back(j + 1);
            S.second+=energia[i][j+1];
            encontrarSeamBacktrackingRec(energia, i + 1, j + 1, n, m, S, B);
            S.second-=energia[i][j+1];
            S.first.pop_back();
        }
    }

    else{
        return;
    }    
}    


// función principal
std::vector<int> encontrarSeamBacktracking(const std::vector<std::vector<double>>& energia) {
    if (energia.empty() || energia[0].empty()) {
        return {};
    }

    int n= energia.size();                  // filas
    int m= energia[0].size();               // columnas

    std::pair<std::vector<int>,double> B;   // mejor camino encontrado
    B.second=std::numeric_limits<double>::infinity();

    for (int j = 0; j < m; j++) {           // comenzando desde cada columna posible en la primer fila
        std::pair<std::vector<int>,double> S;
        S.first.push_back(j);
        S.second = energia[0][j];
        encontrarSeamBacktrackingRec(energia, 1, j, n, m, S, B);
    }
    
    return B.first;
}