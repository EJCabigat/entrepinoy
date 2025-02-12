@echo off
pyinstaller main.py --onefile
rmdir /s /q release\alpha
mkdir release\alpha
copy NUL release\alpha\.gitkeep
move build release\alpha
move dist release\alpha
del main.spec
mkdir "release\alpha\entrepinoy"
move release\alpha\dist\main.exe release\alpha\entrepinoy
mkdir release\alpha\entrepinoy\assets
xcopy /e assets release\alpha\entrepinoy\assets\
mkdir release\alpha\entrepinoy\game
xcopy /e game release\alpha\entrepinoy\game\
xcopy region.py release\alpha\entrepinoy
xcopy scene_builder.py release\alpha\entrepinoy
xcopy setting.py release\alpha\entrepinoy
cd release\alpha\entrepinoy
main
cd ../../..
cmd -k