import os
import subprocess
import numpy as np
import shutil

def generate_video(input_path, prefix, iter_, id_, char_id=0, image_synthesis=['normal'], frame_rate=5, output_path=None):
    """ Generate a video of an episode """
    if output_path is None:
        output_path = input_path
    
    output_path = os.path.join(output_path, str(iter_))
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    input_path = os.path.join(input_path, str(iter_))
    vid_folder = '{}/{}/{}/'.format(input_path, prefix, char_id)
    # print(os.path.exists(output_path))
    # print(os.path.exists(vid_folder))
    if not os.path.exists(vid_folder):
        print("The input path: {} you specified does not exist.".format(input_path))
    else:
        for vid_mod in image_synthesis:
            command_set = ['ffmpeg', '-i',
                             '{}/Action_%04d_0_{}.png'.format(vid_folder, vid_mod),                              
                             '-r', str(frame_rate),
                             '-pix_fmt', 'yuv420p',
                             '{}/video_{}_{}_{}.mp4'.format(output_path, vid_mod, iter_, id_)]
            subprocess.call(command_set)
            print("Video generated at ", '{}/video_{}_{}_{}.mp4'.format(output_path, vid_mod, iter_, id_))

def read_pose_file(file_name, prefix):
    with open('{}/pd_{}.txt'.format(file_name, prefix), 'r') as f:
        content = f.readlines()[1:]

    pose = []
    for l in content:
        pose.append(np.array([float(x) for x in l.split(' ')]))
    return pose

def get_skeleton(input_path, prefix, char_id=0):
    skeleton_file = '{}/{}/{}/'.format(input_path, prefix, char_id)
    skeleton_content = read_pose_file(skeleton_file, prefix)
    pose_char = np.array(skeleton_content)[:, 1:]
    frame_index = np.array(skeleton_content)[:, 1:]
    pose_char = pose_char.reshape((pose_char.shape[0], -1, 3))
    valid_pose = pose_char.sum(-1).sum(0) != 0
    return pose_char[:, valid_pose, :], frame_index
