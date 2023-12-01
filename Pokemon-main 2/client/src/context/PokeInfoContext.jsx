import React, { createContext, useContext, useState } from 'react'

const PokeInfoContext = createContext({
    pokemons: [],
    selectPks: [],
    resultPks: [],
    pokemonsUpdate: () => Promise,
    selectPksUpdate: () => Promise,
    resultPksUpdate: () => Promise
});

export function PokeInfoProvider({children}){
    const [pokemons, setPokemons] = useState([]);
    const [selectPks, setSelectPks] = useState([]);
    const [resultPks, setResultPks] = useState([]);
    function updatePokemons(newPokemon)
    {
        setPokemons(newPokemon);
    }
    function updateSelectPks(newSelect)
    {
      setSelectPks(newSelect);
    }
    function updateResultPks(newResult)
    {
      setResultPks(newResult);
    }

    const contexValue = 
    {
        pokemons: pokemons,
        selectPks: selectPks,
        resultPks: resultPks,
        pokemonsUpdate: updatePokemons,
        selectPksUpdate: updateSelectPks,
        resultPksUpdate: updateResultPks
    }
  return (
    <PokeInfoContext.Provider value = {contexValue}>
      {children}
    </PokeInfoContext.Provider>
  )
}
export function usePokemonInfo()
{
    return useContext(PokeInfoContext);
}



