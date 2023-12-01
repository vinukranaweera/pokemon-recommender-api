import React from 'react'
import Pokeball from "../image/pokeball.png";
import { usePokemonInfo } from '../context/PokeInfoContext';
import axios from "axios";

const PokeButton = ({className}) => {
  function getRandomInt(max) {
    return Math.floor(Math.random() * max);
  }
  const {selectPks, resultPks, resultPksUpdate} = usePokemonInfo();
  //convert selected pokemons to post req body form
  const generateJson = () => {
    let json = {
      "columns": ["Generation","Status","Against Normal","Against Fire","Against Water","Against Electric","Against Grass","Against Ice","Against Fighting","Against Poison","Against Ground","Against Flying","Against Psychic","Against Bug","Against Rock","Against Ghost","Against Dragon","Against Dark","Against Steel","Against Fairy"],
      "index": [...Array(selectPks.length).keys()],
      "data": selectPks.map((pk) => ([
        pk["Generation"],
        pk["Status"],
        pk["Against Normal"],
        pk["Against Fire"],
        pk["Against Water"],
        pk["Against Electric"],
        pk["Against Grass"],
        pk["Against Ice"],
        pk["Against Fighting"],
        pk["Against Poison"],
        pk["Against Ground"],
        pk["Against Flying"],
        pk["Against Psychic"],
        pk["Against Bug"],
        pk["Against Rock"],
        pk["Against Ghost"],
        pk["Against Dragon"],
        pk["Against Dark"],
        pk["Against Steel"],
        pk["Against Fairy"]
      ]))
    }
    return json;
  }
  const handleClick = async () => {
    resultPksUpdate([]);
    const SPRITE = (num) => `https:/raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${num}.png`;
    const RECOM_API = (name) => `http://127.0.0.1:5000/recommendations/${name}`
    const RECOM_APIs = selectPks.map((ea) => RECOM_API(ea["Name"]))
    const requests = RECOM_APIs.map((API) => axios.get(API));
    const responses = await Promise.all(requests);
    responses.forEach((ea) => {
      const data = ea.data;
      const poke = {
        "Name": data["Name"],
        "spriteUrl": SPRITE(data["Pokedex Number"]),
        "Primary Type": data["Primary Type"],
        "Secondary Type": data["Secondary Type"] 
      }
      resultPksUpdate((prev) => [...prev, poke]);
   });
  }
  return (
    <button className = {className} onClick={handleClick}>
      <img src = {Pokeball}/>
    </button>
  )
}

export default PokeButton
