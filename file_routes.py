import os
import mimetypes
from flask import Blueprint, render_template, request, send_file, abort, current_app

file_browser = Blueprint('file_browser', __name__)

def get_drives():
    drives = []
    if os.name == 'nt':
        for drive in range(ord('A'), ord('Z')+1):
            letter = chr(drive)
            if letter.upper() == 'C':
                continue
            drive_letter = f"{letter}:\\"
            if os.path.exists(drive_letter):
                drives.append(drive_letter)
    else:
        drives.append('/')
    return drives

@file_browser.route('/browse')
@file_browser.route('/browse/<path:subpath>')
def browse(subpath=None):
    if subpath is None:
        # List drives on Windows
        drives = get_drives()
        return render_template('file_browser.html', files=drives, current_path="", is_root=True)
    
    # Security check: Block C drive
    if os.name == 'nt':
        norm_path = subpath.replace('/', '\\').upper()
        if norm_path.startswith('C:') or norm_path.startswith('C\\'):
             return "Access to C: drive is disabled for security.", 403

    # Construct full path
    # On Windows, subpath usually comes like "C:/Users/..." or "C:\Users\..."
    # Flask might strip the drive colon if not careful, but path converter usually handles it.
    
    # If subpath is just a drive letter (e.g. "C:"), append slash
    if os.name == 'nt' and len(subpath) == 2 and subpath[1] == ':':
        subpath += '\\'
        
    abs_path = subpath
    
    if not os.path.exists(abs_path):
        return f"Path not found: {abs_path}", 404
        
    if os.path.isfile(abs_path):
        return send_file(abs_path)
        
    try:
        items = os.listdir(abs_path)
        files = []
        dirs = []
        
        for item in items:
            item_path = os.path.join(abs_path, item)
            is_dir = os.path.isdir(item_path)
            
            # Format path for URL (forward slashes)
            url_path = item_path.replace('\\', '/')
            
            entry = {
                'name': item,
                'path': url_path,
                'is_dir': is_dir,
                'type': 'dir' if is_dir else 'file'
            }
            
            if is_dir:
                dirs.append(entry)
            else:
                # Check extension for viewability
                ext = os.path.splitext(item)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    entry['type'] = 'image'
                elif ext in ['.mp4', '.webm', '.ogg']:
                    entry['type'] = 'video'
                elif ext in ['.pdf']:
                    entry['type'] = 'pdf'
                files.append(entry)
                
        parent_path = os.path.dirname(abs_path)
        
        # Robustly check if we are at the root of a drive (e.g. C:, C:\, C:/)
        is_drive_root = False
        if os.name == 'nt':
            # Check if path looks like X: or X:\ or X:/
            if len(abs_path) <= 3 and len(abs_path) >= 2 and abs_path[1] == ':':
                 is_drive_root = True
        elif abs_path == '/':
            is_drive_root = True
            
        if is_drive_root:
             parent_path = None
             
        return render_template('file_browser.html', 
                             dirs=dirs, 
                             files=files, 
                             current_path=abs_path, 
                             parent_link=parent_path.replace('\\', '/') if parent_path else None,
                             is_root=False)
                             
    except PermissionError:
        return "Permission Denied", 403
    except Exception as e:
        return str(e), 500

@file_browser.route('/view/<path:filepath>')
def view_file(filepath):
    # Security check: Block C drive
    if os.name == 'nt':
        norm_path = filepath.replace('/', '\\').upper()
        if norm_path.startswith('C:') or norm_path.startswith('C\\'):
             return "Access to C: drive is disabled for security.", 403

    # Depending on how the browser constructs the path, we might need to fix it
    if not os.path.exists(filepath):
        return "File not found", 404
    return send_file(filepath)
