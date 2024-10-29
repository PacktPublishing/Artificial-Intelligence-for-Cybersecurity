# Reference from AndNetMnist, https://github.com/PegX/HP-MDC/tree/main/network_traffic/create_data
import tensorflow as tf
import tensorflow_datasets as tfds

(pcap_data_train, pcap_data_test), pcap_ds_info = \
    tfds.load(
        'pcap_mnist', split= ['train', 'test'],
        shuffle_files=True, as_supervised=True,
        with_info=True,
)
def pcap_normalize_data(pcap_image, pcap_label):
    return tf.cast(pcap_image, tf. float32)/255., pcap_label

pcap_data_train = pcap_data_train.map(pcap_normalize_data,
                                      num_parallel_calls=tf.data.AUTOTUNE)
pcap_data_test = pcap_data_test.map(normalize_data,
                                    num_parallel_calls=tf.data.AUTOTUNE)

model = tf.keras.models.Sequential([tf.keras.layers.Flatten(input_ shape= (28,28)),tf.keras.layers.Dense(128, activation='relu'), tf.keras.layers.Dense(10)]
)
# Model define
model.compile(optimizer=tf.keras.optimizers.Adam(0.001),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=[tf.keras.metrics.SparseCategoricalAccurary()],)
# Model train
model.fit(pcap_data_train, epochs=6)

# Model Predict/test
model.predict(pcap_data_test)