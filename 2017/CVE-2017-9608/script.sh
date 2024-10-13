sudo rm -rf out &&
sudo docker build -t ffmpeg_image . && 
sudo docker run --rm -v $PWD/out:/workspace/out --name ffmpeg_container ffmpeg_image &&
sudo cp out/* . &&
sudo rm -rf out
