class Room:
    def __init__(self, top_left=None, top_right=None, bottom_left=None, bottom_right=None):
        self._top_left = top_left
        self._top_right = top_right
        self._bottom_left = bottom_left
        self._bottom_right = bottom_right

    # Getters
    def get_top_left(self):
        return self._top_left

    def get_top_right(self):
        return self._top_right

    def get_bottom_left(self):
        return self._bottom_left

    def get_bottom_right(self):
        return self._bottom_right

    # Setters
    def set_top_left(self, top_left):
        self._top_left = top_left

    def set_top_right(self, top_right):
        self._top_right = top_right

    def set_bottom_left(self, bottom_left):
        self._bottom_left = bottom_left

    def set_bottom_right(self, bottom_right):
        self._bottom_right = bottom_right

    def is_room_valid(self):
        return all([self._top_left, self._top_right, self._bottom_left, self._bottom_right])
