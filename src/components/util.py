def clamp(value: float, min: float, max: float) -> float:
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value