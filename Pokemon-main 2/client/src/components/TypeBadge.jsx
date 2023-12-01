import React from 'react'

const TypeBadge = (props) => {
    const badgeStyle = new Map([
        ["Normal", "bg-[#a8a77a] border-t-[#c6c6a8] border-b-[#818054]"],
        ["Fire", "bg-[#ee8130] border-t-[#f4ac77] border-b-[#c25c10]"],
        ["Water", "bg-[#6390f0] border-t-[#a9c2f7] border-b-[#1d5ee9]"],
        ["Electric", "bg-[#f7d02c] border-t-[#fae076] border-b-[#cfa808]"],
        ["Grass", "bg-[#7ac74c] border-t-[#a5d986] border-b-[#56972f]"],
        ["Ice", "bg-[#96d9d6] border-t-[#ceedec] border-b-[#5ec5c0]"],
        ["Fighting", "bg-[#c22e28] border-t-[#dd5f5a] border-b-[#831f1b]"],
        ["Poison", "bg-[#a33ea1] border-t-[#c668c4] border-b-[#6c296a]"],
        ["Ground", "bg-[#e2bf65] border-t-[#eedaa5] border-b-[#d3a328]"],
        ["Flying", "bg-[#a98ff3] border-t-[#ded4fa] border-b-[#744aec]"],
        ["Psychic", "bg-[#f95587] border-t-[#fc9fbb] border-b-[#f60b53]"],
        ["Bug", "bg-[#a6b91a] border-t-[#d0e43c] border-b-[#6a7611]"],
        ["Rock", "bg-[#b6a136] border-t-[#d2c067] border-b-[#7b6d24]"],
        ["Ghost", "bg-[#735797] border-t-[#9a83b8] border-b-[#4e3b66]"],
        ["Dragon", "bg-[#6f35fc] border-t-[#a580fd] border-b-[#4403e1]"],
        ["Dark", "bg-[#705746] border-t-[#9e7c64] border-b-[#413229]"],
        ["Steel", "bg-[#b7b7ce] border-t-[#e5e5ed] border-b-[#8989af]"],
        ["Fairy", "bg-[#d685ad] border-t-[#e9bed3] border-b-[#c34c86]"],
    ]);
    const divStyle = "font-bold w-[6rem] text-center inline-block border-transparent border-solid border-[.1em] pt-[.1em] px-[.2em] pb-[.2em] my-[.1em] mx-[.015em] rounded-[.4em] " + badgeStyle.get(props.pokeType);
  return (
    <div className = {divStyle}>
      <span className = "uppercase text-[.8em] text-white drop-shadow">{props.pokeType}</span>
    </div>
  )
}

export default TypeBadge
