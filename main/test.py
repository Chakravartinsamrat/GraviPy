import glfw
from OpenGL.GL import *
import numpy as np
import sys



def start_glfw():
    # Initialize GLFW
    if not glfw.init():
        print("Failed to initialize GLFW")
        sys.exit(1)
    
    # idhar canvas size specify karna hai
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    
    
    window = glfw.create_window(800, 600, "OpenGL Window", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        sys.exit(1)
    
    glfw.make_context_current(window)
    
    return window

def create_vbo_vao(vertices):
    """Create Vertex Buffer Object (VBO) and Vertex Array Object (VAO)."""
   
    VAO = glGenVertexArrays(1)
    
    VBO = glGenBuffers(1)
    
    glBindVertexArray(VAO)
    
    # Pooints (VBO) ko canvas(VAO) mein put kiya
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), None)
    glEnableVertexAttribArray(0)
    
    # Unbind VBO and VAO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    
    return VAO, VBO

def create_shader_program(vertex_shader_source, fragment_shader_source):
    """Create and compile shader program."""
    
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_source)
    glCompileShader(vertex_shader)
    
    
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_source)
    glCompileShader(fragment_shader)
    
    
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    
    # Delete shaders as they're now linked to the program
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    return shader_program

def main():
    # Window Banaya
    window = start_glfw()
    
    # add points
    vertices = np.array([
        -0.5, -0.5, 0.0,  # bottom left
         0.5, -0.5, 0.0,  # bottom right
         0.0,  0.5, 0.0   # top center
    ], dtype=np.float32)
    
    # create VAO and VBO
    VAO, VBO = create_vbo_vao(vertices)
    
    # (Think of this as GPS coordinates)
    vertex_shader_source = """
    #version 330 core    
    layout (location = 0) in vec3 aPos;
    void main() {
        gl_Position = vec4(aPos, 1.0);
    }
    """
    
    
    fragment_shader_source = """
    #version 330 core
    out vec4 FragColor;
    void main() {
        FragColor = vec4(1.0, 0.5, 0.2, 1.0);  // Orange color
    }
    """
    
    shader_program = create_shader_program(vertex_shader_source, fragment_shader_source)
    
    # put all points in render
    while not glfw.window_should_close(window):
    
        glfw.poll_events()
        # clear the screen
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # draw the triangle
        glUseProgram(shader_program)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        # update canvas
        glfw.swap_buffers(window)
    
    # Clean up
    glDeleteVertexArrays(1, [VAO])
    glDeleteBuffers(1, [VBO])
    glDeleteProgram(shader_program)
    
    glfw.terminate()

if __name__ == "__main__":
    main()