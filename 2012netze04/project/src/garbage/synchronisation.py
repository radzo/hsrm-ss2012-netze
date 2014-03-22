# usr/bin/python
# -*- coding: utf-8 -*-

import settings, time, os, shutil
from logging import logActivity
        
def sync(groupname, folder1, folder2):
    logActivity(groupname, comment="Die Synchronisierung des Ordners >>" + groupname + "<< wird gestartet!")

    if settings.DEBUG == 1:
        logActivity(groupname, comment="Ein Kommentar")
        logActivity(groupname, "addFile", "Dateiname")
        logActivity(groupname, "removeFile", "Dateiname")
        logActivity(groupname, "update", "Dateiname", modifiedDate=time.strftime("%d.%m.%Y um %H:%M:%S Uhr"))
    
    sync_dirs(groupname, folder1, folder2);

def sync_dirs(groupname, source, dest):
    
    ## Wenn der Zielordner nicht exisitert, einen erstellen
    if not os.path.exists(dest):
        os.makedirs(dest)
    
    ## Ordnerstruktur auslesen  
    def read_directories(where):
        all_dirs, all_files = [], []
        
        for root, dirs, files in os.walk(where):
            for dir in dirs:
                abs_dir = os.path.join(root, dir)
                rel_dir = os.path.relpath(abs_dir, where);
                all_dirs.append((abs_dir, rel_dir))
            for file in files:
                abs_file = os.path.join(root, file)
                rel_file = os.path.relpath(abs_file, where)
                all_files.append((abs_file, rel_file))
        return (all_dirs, all_files)
    
    left_dirs, left_files = read_directories(source)
    right_dirs, right_files = read_directories(dest)
    
    ## Ordner links -> rechts synchronisieren
    for left_dir in left_dirs:
        rel_path = left_dir[1]
        equivalent_right_dir = filter(lambda e:e[1] == rel_path, right_dirs)
        ## Wenn der Ordner nicht auf der rechten Seite existiert, Ordner auf der rechten Seite erstellen
        if len(equivalent_right_dir) == 0:
            os.makedirs(os.path.join(dest, rel_path))
            logActivity(groupname, "addFolder", rel_path, "remote")

    ## Ordner rechts -> links synchronisieren
    for right_dir in right_dirs:
        rel_path = right_dir[1]
        equivalent_left_dir = filter(lambda e:e[1] == rel_path, left_dirs)
        ## Wenn der Ordner nicht auf der rechten Seite existiert, Ordner auf der rechten Seite erstellen
        if len(equivalent_left_dir) == 0:
            os.makedirs(os.path.join(source, rel_path))
            logActivity(groupname, "addFolder", rel_path, "local")
    
    
    ## Anfänge für löschen linksseitig von Ordnern
    #for right_dir in right_dirs:
    #   rel_path = right_dir[1]
    #  equivalent_left_dir = filter(lambda e:e[1] == rel_path, left_dirs)
    # if(len(equivalent_left_dir) == 0) and (os.path.exists(right_dir[0])):
    #    shutil.rmtree(right_dir[0])
    
    ## Dateien links -> rechts synchronisieren
    for left_file in left_files:
        rel_path = left_file[1]
        equivalent_right_file = filter(lambda e:e[1] == rel_path, right_files)
        ## Wenn die Datei nicht auf der rechten Seite existiert, Datei auf die rechten Seite kopieren
        if len(equivalent_right_file) == 0:
            shutil.copyfile(left_file[0], os.path.join(dest, rel_path))
            logActivity(groupname, "addFile", rel_path, "remote")

        ## Wenn die Datei schon existiert..
        else:
            left_content = open(left_file[0], "rb").read()
            right_content = open(equivalent_right_file[0][0], "rb").read()
            ## Wenn der Inhalt der Datei linksseitig neuer ist als der Inhalt rechtsseitig, remote überschreiben
            if left_content != right_content and os.path.getmtime(left_file[0]) > os.path.getmtime(equivalent_right_file[0][0]):
                shutil.copyfile(left_file[0], os.path.join(dest, rel_path))
                logActivity(groupname, "update", rel_path, "remote", modifiedDate=os.path.getmtime(left_file[0]))
            ## Wenn der Inhalt der Datei rechtsseitig neuer ist als der Inhalt linksseitig, lokal überschreiben
            if left_content != right_content and os.path.getmtime(left_file[0]) < os.path.getmtime(equivalent_right_file[0][0]):
                shutil.copyfile(equivalent_right_file[0][0], os.path.join(source, rel_path))
                logActivity(groupname, "update", rel_path, "local", modifiedDate=os.path.getmtime(equivalent_right_file[0][0]))
            

    ## Dateien rechts -> links synchronisieren
    for right_file in right_files:
        rel_path = right_file[1]
        equivalent_left_file = filter(lambda e:e[1] == rel_path, left_files)
        ## Wenn die Datei nicht auf der rechten Seite existiert, Datei auf die rechten Seite kopieren
        if len(equivalent_left_file) == 0:
            shutil.copyfile(right_file[0], os.path.join(source, rel_path))
            logActivity(groupname, "addFile", rel_path, "local")

        ## Wenn die Datei schon existiert..
        else:
            right_content = open(right_file[0], "rb").read()
            left_content = open(equivalent_left_file[0][0], "rb").read()
            ## Wenn der Inhalt der Datei linksseitig neuer ist als der Inhalt rechtsseitig, remote überschreiben
            if right_content != left_content and os.path.getmtime(right_file[0]) > os.path.getmtime(equivalent_left_file[0][0]):
                shutil.copyfile(right_file[0], os.path.join(source, rel_path))
                logActivity(groupname, "update", rel_path, "local", modifiedDate=os.path.getmtime(left_file[0]))
            ## Wenn der Inhalt der Datei rechtsseitig neuer ist als der Inhalt linksseitig, lokal überschreiben
            if right_content != left_content and os.path.getmtime(right_file[0]) < os.path.getmtime(equivalent_left_file[0][0]):
                shutil.copyfile(equivalent_left_file[0][0], os.path.join(dest, rel_path))
                logActivity(groupname, "update", rel_path, "remote", modifiedDate=os.path.getmtime(equivalent_left_file[0][0]))
            


    ## Anfänge für löschen linksseitig von Dateien
    #for right_file in right_files:
    #    rel_path = right_file[1]
    #    equivalent_left_file = filter(lambda e:e[1] == rel_path, left_files)
    #    if (len(equivalent_left_file) == 0) and (os.path.exists(right_file[0])):
    #        os.unlink(right_file[0])
