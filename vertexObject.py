class vertexObject:
  def __init__(self, curr_vertex, g_value = -1.0, parent_vertex = None):
    self.curr_vertex = curr_vertex
    self.g_value = g_value
    self.parent = parent_vertex