import os

path = 'frame_interpolation/pretrained_models/film_net/Style/saved_model'
folder = 'photos' #@param {type:"string"}

times = 10 #@param {type:"slider", min:1, max:10, step:1}
fps = 30 #@param {type:"slider", min:1, max:60, step:1}

# Resize images

for current_path in os.listdir(folder):
    if os.path.isfile(os.path.join(folder, current_path)):
        os.system(f"""
          ffmpeg -y -i {folder}/{current_path} -vf scale="700:-1" {folder}/{current_path.replace('jpg', 'jpg')}
        """)

print('Interpolating...')
# update! httplib2==0.20.2

os.system(f"""
  python -m frame_interpolation.eval.interpolator_cli \
      --pattern {folder} \
      --fps {fps} \
      --model_path {path} \
      --times_to_interpolate {times} \
      --output_video
""")

# create boomerang

os.system(f"""
  ffmpeg -y -i {folder}/interpolated.mp4 \
      -filter_complex "[0]reverse[r];[0][r]concat=n=2:v=1:a=0,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
      {folder}/interpolated.gif
""")