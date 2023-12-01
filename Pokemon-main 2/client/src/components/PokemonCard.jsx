import React from 'react'
import TypeBadge from './TypeBadge'
import { usePokemonInfo } from '../context/PokeInfoContext';

const PokemonCard = (props) => {
  const {selectPks, selectPksUpdate} = usePokemonInfo();
  const removePoke = () => {
    const newSelect = selectPks.filter((ea) => ea["Name"] != props.name)
    selectPksUpdate(newSelect);
  }
  return (
    <div className="bg-gradient-to-r from-[#edfedb] to-[#92f91b] flex flex-row rounded-lg">
      <img src = {props.spriteUrl}></img>
      <div className="flex flex-col">
        <span>{props.name}</span>
        <div><TypeBadge pokeType = {props.primary}/> / <TypeBadge pokeType = {props.secondary}/></div>
      </div>
      <button className={"bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center" + props.hidden} onClick = {removePoke}>
        X
      </button>
    </div>
  )
}

export default PokemonCard