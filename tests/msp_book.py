
"""Run the real MSP executable on a shared-spine graph; no injected schedule."""
import os
from pathlib import Path
import subprocess
import sys
import tempfile

exe=str(Path(sys.argv[1]).resolve())
with tempfile.TemporaryDirectory() as folder:
    folder=Path(folder)
    graph=folder/'book.metis'
    graph.write_text('7 11\n2 3 4 5 6 7\n1 3 4 5 6 7\n1 2\n1 2\n1 2\n1 2\n1 2\n')
    for threads in (1,2,4):
        for repeat in range(100):
            output=folder/'labels.txt'
            result=subprocess.run([exe,'-kttype=msp','-iftype=metis',str(graph),str(output)],
                env=dict(os.environ,OMP_NUM_THREADS=str(threads),OMP_DYNAMIC='FALSE'),
                capture_output=True,text=True,timeout=10,check=True)
            rows=[tuple(map(int,line.split())) for line in output.read_text().splitlines()]
            assert len(rows)==11,(threads,repeat,rows)
            expected={(1,2)} | {(side,leaf) for side in (1,2) for leaf in range(3,8)}
            assert {(min(u,v),max(u,v)) for u,v,label in rows}==expected,(threads,repeat,rows)
            assert all(label==3 for u,v,label in rows),(threads,repeat,rows)
print('MSP book: 300 runs passed (1, 2 and 4 threads)')
