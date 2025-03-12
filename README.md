# pysokoban-fuzz

http://www.linusakesson.net/games/autosokoban/board.php?v=1&seed=1179617834&level=1

## deps
```
git clone https://github.com/AFLplusplus/LibAFL.git
cd LibAFL

rustup update stable
cargo build --release
cd bindings/pylibafl

pip install -U meson maturin

maturin build --release
pip install target/wheels/PyLibAFL-*.whl


pip install beautifulsoup4 requests
```


