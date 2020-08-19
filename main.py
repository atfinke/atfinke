import argparse
import pylast

parser = argparse.ArgumentParser()
parser.add_argument("API_KEY")
parser.add_argument("API_SECRET")
parser.add_argument("USERNAME")
parser.add_argument("PASSWORD")
parser.add_argument("TRACKS")
args = parser.parse_args()

password_hash = pylast.md5(args.PASSWORD)
network = pylast.LastFMNetwork(api_key=args.API_KEY, api_secret=args.API_SECRET,
                               username=args.USERNAME, password_hash=password_hash)

tracks = network.get_user(args.USERNAME).get_recent_tracks(limit=int(args.TRACKS))

image_size = "16%"
output = "### Recent Tracks\n"

for index, playedTrack in enumerate(tracks):
    track = playedTrack.track
    
    track_name = track.get_name()
    track_url = track.get_url()
    
    image_url = None
    try:
      image_url = track.get_cover_image()
    except:
      pass

    if image_url is None:
        image_url = "https://github.com/atfinke/atfinke/blob/master/placeholder.jpeg?raw=true"


    output += "[<img src='{}' width='{}' height='{}' alt='{}'>]({})&nbsp;&nbsp;&nbsp;&nbsp;".format(image_url, image_size, image_size, track_name.replace("'", ""), track_url)
    if index % 5 == 4:
        output += "<br>"

with open("README.md", "w") as file:
    file.write(output)
