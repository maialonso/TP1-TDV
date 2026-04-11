#include "ProgramacionDinamica.h"
#include <limits>
#include <vector>


// función recursiva
std::pair<int, double> encontrarSeamPDRec(const std::vector<std::vector<double>>& energia, int i, int j, int n, int m, std::vector<std::vector<std::pair<int, double>>>& memo) {
    if(memo[i][j].second != std::numeric_limits<double>::infinity()){   // si ya resolvió este subproblema reutiliza el resultado (memorización)
        return memo[i][j];
    }

    if(i==0){                           // caso base: está en la primera fila 
        std::pair<int, double > res = {-1, energia[i][j]};
        memo[i][j]= res;
        return res;
    }
    
    std::pair<int, double> min = {-1, std::numeric_limits<double>::infinity()};
    int mejor;

    if(j > 0 && j < m-1){                       // si no está en un borde 
        for(int k=j-1; k <= j+1; k++){          // recurisón por {j-1, j, j+1}
            std::pair<int, double> aux = encontrarSeamPDRec(energia, i-1, k, n , m, memo); 
            if(min.second > aux.second){         //compara energías
                min = aux;
                mejor = k;
                }
        }
    }

    else if(j==0){                              // si está en la primer columna a la izquierda
        for(int k=j; k <= j+1; k++){           // recursión por {j, j+1}
            std::pair<int, double> aux = encontrarSeamPDRec(energia, i-1, k, n , m, memo);
            if(min.second>aux.second){
                min=aux;
                mejor=k;
            }
        }  
    }

    else{                                      // si está en la última columna a la derecha
        for(int k=j-1; k <= j; k++){           // recursión por {j-1, j}
            std::pair<int, double> aux = encontrarSeamPDRec(energia, i-1, k, n , m, memo); 
            if(min.second>aux.second){
                min=aux;
                mejor= k;
            }
        }
    }

        min.first = mejor;              // guarda la posición del elemento de donde vino
        min.second += energia[i][j];    // suma la energia acumulada hasta ahí
        memo[i][j] = min;                // actualiza memo
        return memo[i][j];
}


// funcion para invertir la solución dado que en la reconstrucción queda como primer posición el último elemento del camino
std::vector<int> invertirPairs(std::vector<int> aInvertir){
    std::vector<int> res;
    for(int i=aInvertir.size()-1; i>=0; i--){       //devuelve el vector en orden (primer elemento el primer elemento del camino)
        res.push_back(aInvertir[i]);
    }
    return res;
}


// función que arma un vector del camino de la costura óptima
std::vector<int> reconstruccion(const std::vector<std::vector<double>>& energia, std::vector<std::vector<std::pair<int, double>>> &memo, int colInicio){
    int i= energia.size()-1;        // empieza en la última fila
    int j= colInicio;               // columna con menor energía acumulada
    std::vector<int> respuesta; 
    respuesta.push_back({i,colInicio});     //obs: el vector queda invertido
    i--;
    while(i >= 0){
        int posAnterior= memo[i][j].first;  // valor de la pos del elemento anterior
        respuesta.push_back(posAnterior);
        j = posAnterior;//actualizo la columna en donde estoy
        i--;
    }

    //llamo a la funcion que invierte la solucion, asi se devuelve el vector en el orden esperado
    std::vector<int> res= invertirPairs(respuesta);
    return res;

}

std::vector<int> encontrarSeamPDNueva(const std::vector<std::vector<double>>& energia) {
    if (energia.empty() || energia[0].empty()) {
        return {};
    }
    //creo el memo
    int n= energia.size();
    int m= energia[0].size();
    //memo= vector de vectores pair<int: columna "de donde viene", double: energia acumulada>
    std::vector<std::vector<std::pair<int, double>>> memo(
    n,
    std::vector<std::pair<int, double>>(m, {-1, std::numeric_limits<double>::infinity()}));

    //se hace un llamado de la auxiliar por columna
    for(int j = 0; j < m; j++){
        encontrarSeamPDRec(energia, n-1, j, n, m, memo);
    }   
    
    /*ahora busco el minimo-> luego del primer ciclo, todos los elementos de la ultima fila 
      ya estan resueltos con los minimos caminos llenos de energia*/

    //primer elemento de la ultima fila del memo(primer valor posible)
    std::pair<int, double> min= memo[n-1][0];
    
    //posicion con la que voy a hacer la recursion para reconstruir el camino
    int pos=0;

    //empiezo a comparar desde el primero
    for(int i=1; i<m; i++){
        if(min.second>memo[n-1][i].second){
            min = memo[n-1][i];
            pos = i;
        }
    }

    //hago para la reconstruccion
    std::vector<int> posColumna= reconstruccion(energia, memo, pos);
    return posColumna;
}