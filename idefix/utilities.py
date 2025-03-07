
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def shift_columns(nested_lists, shifts):
    if not nested_lists or not shifts:
        return []

    num_rows = len(nested_lists)
    num_cols = len(nested_lists[0])

    # Ensure all inner lists have the same length
    if not all(len(sublist) == num_cols for sublist in nested_lists):
        raise ValueError("All lists in nested_lists must have the same length")

    # Ensure the shifts list has the same length as the number of columns
    if len(shifts) != num_cols:
        raise ValueError(
            "The shifts list must have as many elements as there are columns in nested_lists"
        )

    # Initialize a new list with None values
    shifted = [[None] * num_cols for _ in range(num_rows)]

    for col in range(num_cols):  # Iterate through all columns
        shift = shifts[col]  # Offset for this column

        for row in range(num_rows):  # Iterate through all rows
            new_row = (row + shift) % num_rows  # New position after shifting
            shifted[new_row][col] = nested_lists[row][col]

    return shifted

