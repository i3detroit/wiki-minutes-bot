set windows-powershell := true

# Show this help
@help:
  just --list

# Build & Load the image
build:
  docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) -t localhost/wiki-minutes-bot . --load

# Run a script
run *ARGS:
  docker run -it --rm --env-file ./.env -v $PWD:/wmb localhost/wiki-minutes-bot {{ARGS}}
