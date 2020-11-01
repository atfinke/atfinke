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

tracks = network.get_user(args.USERNAME).get_recent_tracks(limit=int(args.TRACKS) * 2)

image_size = "16%"
output = "### Recent Tracks\n"

valid_track_images = 0

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
        continue

    output += "[<img src='{}' width='{}' height='{}' alt='{}'>]({})&nbsp;&nbsp;&nbsp;&nbsp;".format(image_url, image_size, image_size, track_name.replace("'", ""), track_url)
    if valid_track_images % 5 == 4:
        output += "<br>"
    
    valid_track_images += 1
    if valid_track_images == int(args.TRACKS):
      break

with open("README.md", "w") as file:
    file.write(output)
