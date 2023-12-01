import './App.css';
import { usePokemonInfo } from './context/PokeInfoContext';
import Containter from "./components/Container";
import SearchBar from './components/SearchBar';
import PokemonCardList from './components/PokemonCardList';
import PokeButton from './components/PokeButton';

function App() {
  const {pokemons, selectPks, selectPksUpdate, resultPks} = usePokemonInfo()
  return (
            <div className="bg-[#3466AF] max-h-screen">
              <div className="flex flex-col h-screen justify-center items-center">{/*flex wrapper*/}
                <img src = "https://drive.google.com/uc?export=view&id=16JW-S_WDxEs8DXxp9ZM2ik_DnrakUffP" className= "w-[200px] mx-auto h-[15%]"/>
                <Containter className= "px-5 w-[90%] h-[8%]"><h1 className="text-center font-semibold">Build your best Pokémon team and determine your winning rates!</h1></Containter>
                <div className="flex flex-row h-[75%] w-[90%]">
                  <Containter className = "w-1/3 flex flex-col gap-y-2">
                    <h1 className="text-center font-bold h-[5%]">Build Your Team</h1>
                    <SearchBar/>
                    <PokemonCardList pks = {[...pokemons]} handle = {selectPksUpdate} hidden= " hidden" className="h-[80%]"/>
                  </Containter>
                  {/*<div className = "w-1/3 flex flex-col gap-y-2">*/}
                    <Containter className = "w-1/3 flex flex-col gap-y-2">
                      <h1 className="text-center font-bold h-[5%]">Selection</h1>
                      <PokemonCardList pks = {[...selectPks]} handle = {() => {}} hidden= "" className="h-[80%]"/>
                      <PokeButton className = "w-1/3 place-self-center"/>
                    </Containter>
                  {/*</div>*/}
                  <Containter className = "w-1/3 flex flex-col gap-y-2">
                    <h1 className="text-center font-bold h-[5%]">Result</h1>
                    <PokemonCardList pks = {[...resultPks]} handle = {() => {}} hidden= " hidden" className="h-[80%]"/>
                    </Containter>
                </div>
              </div>
            </div>
  )
}

export default App
