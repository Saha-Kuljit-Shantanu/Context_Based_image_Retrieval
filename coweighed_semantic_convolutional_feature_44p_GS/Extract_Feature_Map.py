def get_channel_feature_map(desired_layer_output, channel):
    feature_map = desired_layer_output[0, :, :, channel]
    return feature_map
def get_feature_map(desired_layer_output, channel_frequency_map, zero_fmap):
  feature_map = zero_fmap
  sum_frequencies = sum(frequency for _, frequency in channel_frequency_map)
  #print(sum_frequencies)
  for channel, frequency in channel_frequency_map:
    feature_map = feature_map + frequency/sum_frequencies * desired_layer_output[0, :, :, channel]
  return feature_map
