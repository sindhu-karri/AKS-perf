import json
import os
from typing import Iterable

from opentelemetry import metrics
from opentelemetry.metrics import CallbackOptions, Observation
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter

with open('/home/nerdywit/fio-kubernetes/benchmark.json') as benchmark_result:
    data = json.load(benchmark_result)

exporter = AzureMonitorMetricExporter(
    connection_string="InstrumentationKey=e6fd0c8e-9dd2-45ee-9d02-0625cb2002e1;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/;ApplicationId=a2305208-7d58-4807-b715-541f8c001765"
)
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))

# Create a namespaced meter
meter = metrics.get_meter_provider().get_meter("aksbenchmark")

import pdb
pdb.set_trace()
for metric_name in data['jobs'][0]['write'].keys():
    counter = meter.create_up_down_counter(metric_name)
    counter.add(data['jobs'][0]['write'][metric_name])

exporter.force_flush()


'''
(Pdb) p data['jobs'][0]['write'].keys()
dict_keys(['io_bytes', 'io_kbytes', 'bw_bytes', 'bw', 'iops', 'runtime', 'total_ios', 'short_ios', 'drop_ios', 'slat_ns', 'clat_ns', 'lat_ns', 'bw_min', 'bw_max', 'bw_agg', 'bw_mean', 'bw_dev', 'bw_samples', 'iops_min', 'iops_max', 'iops_mean', 'iops_stddev', 'iops_samples'])
(Pdb) p data['jobs'][0]['write']['io_bytes']
42949672960
(Pdb) p data['jobs'][0]['write']['iops']
116339.106412
'''


