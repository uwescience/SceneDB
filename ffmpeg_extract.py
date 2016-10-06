import subprocess
import os


def extract_scenes(name, bounds):
    """
    :param name: input filename
    :param bounds: list of tuples (scene_id, start(sec), end(sec)
    :return: output filenames
    """

    files = []

    # Could also run ffmpeg once for all scenes and mutiple outputs
    # http://stackoverflow.com/questions/5651654/ffmpeg-how-to-split-video-efficiently
    for (id, start, end) in bounds:
        basename, _ = os.path.splitext(name)
        outname = "{basename}_{scene}.mp4".format(basename=basename, scene=id)

        # TODO: might experiment with -ss args before and after -i
        p = subprocess.Popen("ffmpeg \
                                    -y \
                                  -ss {start} \
                                  -i {inf} \
                                  -t {duration} \
                                  -c copy \
                                  {outf}".format(
                start=start, duration=end-start, inf=name, outf=outname),
                                  shell=True, stderr=subprocess.PIPE)

        _, p_stderr = p.communicate()

        if p.returncode != 0:
            err_msg = "{0}. Code: {1}".format(p_stderr.strip(), p.returncode)
            raise Exception(err_msg)

        files.append(outname)

    return files

def main():
    # read bounds from a .csv file
    import pandas as pd
    import sys
    bounds = pd.read_csv(sys.argv[2])
    # convert the bounds to list of tuples
    listOfBounds = []
    subsampleRate = 10

    for idx,lb,ub in zip(bounds.index,bounds['LB'],bounds['UB']):
        listOfBounds.append((idx,lb*10/29.7,ub*10/29.7))
    extract_scenes(sys.argv[1],listOfBounds)

if __name__ == '__main__':
    main()
