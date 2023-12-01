import React from 'react'
import PokemonCard from './PokemonCard';

const PokemonCardList = (props) => {

  return (
    <div className={"overflow-auto " + props.className}>
      {(!(props.pks.length === 0)) && 
      <div className="flex flex-col gap-y-1">
        {props.pks.map((poke) => 
        <div onClick = {() => {props.handle((prev) => [...prev, poke])}}>
          <PokemonCard 
          name = {poke["Name"]} 
          spriteUrl = {poke["spriteUrl"]} 
          primary ={poke["Primary Type"]}
          secondary = {poke["Secondary Type"]}
          hidden = {props.hidden}/>
        </div>)}
      </div>
      }
    </div>
  )
}

export default PokemonCardList