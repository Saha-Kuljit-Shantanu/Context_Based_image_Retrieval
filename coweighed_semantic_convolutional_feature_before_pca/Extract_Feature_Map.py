def get_feature_map(desired_layer_output,channel):
    feature_map = desired_layer_output[0, :, :, channel]
    return feature_map

