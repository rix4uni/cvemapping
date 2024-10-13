require "mini_magick"

image = MiniMagick::Image.open("| touch hogehoge.txt", ext="dummy")