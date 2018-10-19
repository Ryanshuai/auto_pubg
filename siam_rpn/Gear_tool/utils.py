import os


def prepare_save_dirs(arg):
    for path_name in dir(arg.save):
        path = getattr(arg.save, path_name)
        if isinstance(path, str) and os.path.isabs(path) and not os.path.exists(path):
            os.makedirs(path)


def create_link(src, dst):
    if not os.path.lexists(dst):
        os.symlink(src, dst)


def prepare_image_site_link_and_visdom_txt(arg):
    if arg.image_site.enable:
        txt = ""
        dirs = (("TrainOut", arg.save.train), ("PeekOut", arg.save.valid), ("TestOut",arg.save.test))
        for title, dirpath in dirs:
            dirname = dirpath.rstrip("/").split('/')[-1]
            name = arg.stamp.experiment_name + "-" + dirname
            create_link(src=dirpath, dst=os.path.join(arg.image_site.data_dir, name))
            url = arg.image_site.url.format(dataset_name=name)
            txt += """ %s <a href='%s'> %s </a></br>""" % (title, url, url)
    else:
        txt = 'image_site is not enabled'
    return txt


if __name__ == '__main__':
    from config.siam_rpn.default import ARG

    arg = ARG()

    prepare_save_dirs(arg)
