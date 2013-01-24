makeindex document.idx
makeindex -s document.ist -t document.glg -o document.gls document.glo
makeindex -s document.ist -t document.abr -o document.abl document.abt
makeindex document.idx