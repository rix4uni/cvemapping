FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=nointeractive

RUN apt-get update -qq && apt-get -y install \
    autoconf \
    automake \
    build-essential \
    cmake \
    git-core \
    libass-dev \
    libfreetype6-dev \
    libgnutls28-dev \
    libmp3lame-dev \
    libsdl2-dev \
    libtool \
    libva-dev \
    libvdpau-dev \
    libvorbis-dev \
    libxcb1-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    meson \
    ninja-build \
    pkg-config \
    texinfo \
    wget \
    yasm \
    zlib1g-dev \
    unzip

WORKDIR /workspace

RUN mkdir -p /workspace/out

RUN wget https://github.com/FFmpeg/FFmpeg/archive/b52b398c30a729dda38c0dd5a0cdeef160c4ca54.zip \
    && unzip b52b398c30a729dda38c0dd5a0cdeef160c4ca54.zip \
    && mv FFmpeg-b52b398c30a729dda38c0dd5a0cdeef160c4ca54 /workspace/ffmpeg

WORKDIR /workspace/ffmpeg

RUN cd /workspace/ffmpeg \
    && ./configure \
    && make -j8

RUN echo "find /workspace/ffmpeg -name \"parser.o\" -type f -exec cp {} /workspace/out/ \;" > /workspace/copy_out.sh \
    && chmod +x /workspace/copy_out.sh

CMD [ "bash", "/workspace/copy_out.sh" ]