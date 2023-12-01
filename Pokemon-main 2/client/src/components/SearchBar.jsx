import React, { useState } from 'react'
import axios from "axios";
import { usePokemonInfo } from '../context/PokeInfoContext';



const SearchBar = () => {
    const {pokemons, pokemonsUpdate} = usePokemonInfo();
    const NAME_ENDPOINT = (name) => `http://127.0.0.1:5000/pokemon?name=${name}`;
    const ID_ENDPOINT = (id) => `http://127.0.0.1:5000/pokemon?id=${id}`
    const TYPE_ENDPOINT = (type) => `http://127.0.0.1:5000/pokemon?type=${type}`
    const SPRITE = (num) => `https:/raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${num}.png`
    const [searchInput, setSearchInput] = useState("");
    const [selectInput, setSelectInput] = useState("Normal");
    const [byName, setbyName] = useState(true);
    const types = ["Normal", "Fire", "Water", "Grass", "Flying", "Fighting", "Poison", "Electric", "Ground", "Rock", "Psychic", "Ice", "Bug", "Ghost", "Steel", "Dragon", "Dark", "Fairy"];
    function isNumeric(value) {
        return /^-?\d+$/.test(value);
    }

    async function getOnePokemon(API){
        const res = await axios.get(API);
        const data = res.data;
        const pk = 
        {
            ...data,
            spriteUrl: SPRITE(data["Pokedex Number"])
        }
        pokemonsUpdate((prev) => [...prev, pk]);
    }
    async function getMultiplePokemons(API){
        const res = await axios.get(API);
        const data = res.data;
        const pks = data.map((ea) => (
            {
                ...ea,
                spriteUrl: SPRITE(ea["Pokedex Number"])
            }
        ))
        pokemonsUpdate((prev) => [...prev, ...pks]);
    }
    async function handleClick(e)
    {
        e.preventDefault();
        pokemonsUpdate([]);
        let API;
        if(byName)
        {
            if(isNumeric(searchInput)) API = ID_ENDPOINT(searchInput)
            else API = NAME_ENDPOINT(searchInput);
            getOnePokemon(API)
        }else
        {   
            API = TYPE_ENDPOINT(selectInput);
            getMultiplePokemons(API);
        }

    }
  return (
    <form className="flex flex-row gap-x-1 h-[10%]">
      <select onChange = {() => setbyName(prev => !prev)} className="bg-blue-400 p-0 w-1/3 flex items-center justify-between font-bold text-xs rounded-lg tracking-wider border-4 border-transparent active:border-white duration-300 active:text-white hover:border-white">
        <option className="font-bold">Name/ID</option>
        <option className="font-bold">Type</option>
      </select>
      {
        byName ?
        (<input value={searchInput} onChange={(e) => {setSearchInput(e.target.value)}} className = "w-2/3 rounded-lg"></input>)
        :
        (<select value={selectInput} onChange={(e) => {setSelectInput(e.target.value)}} className = "w-2/3 rounded-lg">
            {types.map((t) => <option key = {t} value = {t}> {t} </option>)}
        </select>)
      }
        <button className="items-center whitespace-nowrap rounded px-3 py-1.5 cursor-pointer" onClick={handleClick}>
            <svg viewBox="0 0 20 20"  className="h-5 w-5">
                <path fillRule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clipRule="evenodd" />
            </svg>
        </button>
    </form>
  )
}

export default SearchBar