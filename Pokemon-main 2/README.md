# Start

## Client

1. Navigate into `client`: `cd client`
2. Install dependencies: `pnpm install`
3. Run frontend: `pnpm dev`

## Server

Needs `pip`, `python`, `virtualenv` installed

1. Navigate into `server`: `cd server`
2. Create `env` folder: `virtualenv env`
3. Activate the enviornment: run `./env/Scripts/activate` (Windows) or `source env/bin/activate` (Mac)
4. Install packages:
   - `pip install flask pymongo certifi`
5. StartL: `python app.py`
