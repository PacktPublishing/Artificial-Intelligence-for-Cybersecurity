# pip install libselinux-python and then import selinux
import selinux

def get_selinux_context(file_path):
    """Get the SELinux context of a file."""
    try:
        context = selinux.getfilecon(file_path)[1]
        print(f"The current SELinux context of '{file_path}' is: {context}")
        return context
    except OSError as e:
        print(f"Error fetching SELinux context: {e}")
        return None

def set_selinux_context(file_path, new_context):
    """Set the SELinux context of a file."""
    try:
        result = selinux.setfilecon(file_path, new_context)
        if result == 0:
            print(f"Successfully set new SELinux context for '{file_path}': {new_context}")
        else:
            print(f"Failed to set SELinux context for '{file_path}'")
    except OSError as e:
        print(f"Error setting SELinux context: {e}")

# Example usage:
file_path = "/tmp/testfile"

# Get current SELinux context
current_context = get_selinux_context(file_path)

# Set a new SELinux context if necessary (for example, "system_u:object_r:httpd_sys_content_t:s0")
new_context = "system_u:object_r:httpd_sys_content_t:s0"
if current_context:
    set_selinux_context(file_path, new_context)

# Verify the context change
get_selinux_context(file_path)
