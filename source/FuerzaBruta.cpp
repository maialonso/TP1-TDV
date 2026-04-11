#include "FuerzaBruta.h"
#include <limits>
#include <vector>


// función recursiva
void encontrarSeamFuerzaBrutaRec(const std::vector<std::vector<double>>& energia, int i,int j,int n ,int m ,std::vector<int>&S ,std::vector<int>&B, double energiaActual, double& mejorEnergia) {
    if(i==n){               // caso base: es el final de la imagen 
        if(B.empty() || energiaActual < mejorEnergia ){         // si encontró un camino mejor actualiza y guarda ese camino
            mejorEnergia = energiaActual;
            B = S;
        }
        return;
    }

    if(j>0){                // baja por la rama izquierda siempre y cuando no esté en un borde
        S.push_back(j - 1);
        encontrarSeamFuerzaBrutaRec(energia, i + 1, j - 1, n, m, S, B, energiaActual + energia[i][j - 1], mejorEnergia);
        S.pop_back();
    }
    
    S.push_back(j);         // en todos los casos baja por la rama del medio
    encontrarSeamFuerzaBrutaRec(energia, i + 1, j, n, m, S, B, energiaActual + energia[i][j], mejorEnergia);
    S.pop_back();

    if(j<m-1){             // baja por la rama derecha siempre y cuando no esté en un borde
        S.push_back(j + 1);
        encontrarSeamFuerzaBrutaRec(energia, i + 1, j + 1, n, m, S, B, energiaActual + energia[i][j + 1], mejorEnergia);
        S.pop_back();
    }
}


// función principal
std::vector<int> encontrarSeamFuerzaBruta(const std::vector<std::vector<double>>& energia) {
    if (energia.empty()) {
        return {};
    }

    int n= energia.size();          // filas
    int m= energia[0].size();       // columnas

    std::vector<int> B;             // mejor camino encontrado
    double mejorEnergia = std::numeric_limits<double>::infinity();

    for (int j = 0; j < m; j++) {   // comenzando desde cada columna posible en la primer fila
        std::vector<int> S;
        S.push_back(j);
        encontrarSeamFuerzaBrutaRec(energia, 1, j, n, m, S, B, energia[0][j], mejorEnergia);
    }

    for (int i = 0; i < B.size(); i++) {
        B[i] += 1;                  // pasa de base 0 a base 1 (formato de salida)
    }
    return B;
}