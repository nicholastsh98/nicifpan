# Create lists to store datagrams and their indexes

import datetime

import base64
import struct
from classes import EB200header1
from classes import IFPanheader
from dash import dcc, html, dash_table

import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import numpy as np

app = dash.Dash(__name__)
server = app.server


# Create Dash app


# Define layout
app.layout = html.Div([
    html.H1("IFPAN Datagram Analysis"),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        multiple=False,
        max_size=-1,
    ),
    html.Div(id='plotdiv'),
    dcc.Graph(id='plot'),
    dcc.Store(id='x'),
    dcc.Store(id='y'),
    dcc.Store(id='min_data'),
    dcc.Store(id='max_data'),
    dcc.Store(id='time'),
    dcc.Store(id='initial_index'),
    dcc.Store(id='text'),
    dcc.Store(id='micro_symbol'),
    dcc.Store(id='updated_data'),
    dbc.Alert(id='signal-alert', color='info', dismissable=False),
    html.Div(id='index-display'),
    html.Label('Select Index:'),
    html.Div(id='index-slide-id', children=[
        dcc.Interval(id="animate", disabled=True),

        html.Label('Select Index:'),
        dcc.Slider(
            id='index-slider',
            min=0,
            max=0,
            step=1,
            value=0,
            marks={}
        ),
        html.Button("Play/Stop", id="play"),
        html.Div(id='index-display-test')
    ]),
    html.Label('Set Threshold:'),
    dcc.Slider(
        id='threshold-slider',
        min=0,
        max=0,
        value=0,
        tooltip={'placement': 'bottom'}
    ),
    dcc.Checklist(
        id='toggle-y-axis',
        options=[{'label': 'Fixed Y-Axis', 'value': 'fixed-y-axis'}],
        value=['fixed-y-axis']
    ),
    html.Div([
        html.H2('Identified Signals Bandwidths'),
        dash_table.DataTable(
            id='bandwidth-table',
            columns=[
                {'name': 'Signal', 'id': 'Signal'},
                {'name': 'Bandwidth', 'id': 'Bandwidth'},
                {'name': 'Start Frequency', 'id': 'Start Frequency'},
                {'name': 'End Frequency', 'id': 'End Frequency'},
                {'name': 'Center Frequency', 'id': 'Center Frequency'},
                {'name': 'Median Signal Strength', 'id': 'Median Signal Strength'},
            ],
            style_header={
                'text-align': 'center'  # Align column titles in the middle
            },
            style_data={
                'text-align': 'center'  # Align all columns in the middle
            },
            style_table={'overflowX': 'auto'},
        )
    ]),
    html.Div(id='timestamp-output')
])

data=[]
data2=[]
data3=[]
data4=[]
timestampdata=[]
IFPANLIST =[]
@app.callback(
    Output('index-display-test', 'children'),
    #Output('index-display', 'value'),
    Output("index-slider", "value"),
    Input('animate', 'n_intervals'),
    Input('updated_data', 'data'),
    State('index-slider', 'value'),
    prevent_initial_call=True

)
def update_output(n,updated_data,selected_value):
    if updated_data is None:
        return 0,0
    max = len(updated_data) - 1
    if n is None:
        return 0,0
    selected_value = (n%max)* 1
    return 'You have selected "{}"'.format(selected_value), selected_value

@app.callback(
    Output("animate", "disabled"),
    Input("play", "n_clicks"),
    State("animate", "disabled"),
)
def toggle(n, playing):
    if n:
        return not playing
    return playing

class EB200DatagramFormat:
    def __init__(self, magic_number, version_major, version_minor, sequence_number, seq_number_high, data_size,
                 attributes,
                 length, number_of_trace_values, channel_number, optional_header_length, selector_flags):
        self.magic_number = magic_number
        self.version_major = version_major
        self.version_minor = version_minor
        self.sequence_number = sequence_number
        self.seq_number_high = seq_number_high
        self.data_size = data_size
        self.attributes = attributes
        self.length = length
        self.number_of_trace_values = number_of_trace_values
        self.channel_number = channel_number
        self.optional_header_length = optional_header_length
        self.selector_flags = selector_flags
def convert_unix_epoch(value):
    # Create a datetime object from the timestamp in seconds
    timestamp_seconds = value // 10 ** 9
    timestamp_datetime = datetime.datetime.utcfromtimestamp(timestamp_seconds)

    # Format the datetime object as a human-readable string
    human_readable_format = timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return human_readable_format
def IFPANoptionalheaderprint(tag_value,decoded1,index):

    global IFPanoptionalheadinstance, total_datagrams
    if (tag_value == 10501):  # parsing IFPans optional header
        next_104_bytes = decoded1[ index + 18 + 22 + 36:index + 18 + 22 + 36 + 104+ 4]  # reads next 26 bytes of data after attributes

        unpacked_IFPanoptionalheader_attributes = struct.unpack('<I I h h I I i I I Q I I h h Q h h h h H h q q q I I H H', next_104_bytes) #little endian once optional header is reached
        IFPanoptionalheadinstance = IFPanheader(
            unpacked_IFPanoptionalheader_attributes[0], #freq_low
            unpacked_IFPanoptionalheader_attributes[1], #freqspan
            unpacked_IFPanoptionalheader_attributes[2], #avgtime
            unpacked_IFPanoptionalheader_attributes[3], #avgtype
            unpacked_IFPanoptionalheader_attributes[4], #measuretime
            unpacked_IFPanoptionalheader_attributes[5], #freq_high
            unpacked_IFPanoptionalheader_attributes[6], #demodfreqchannel
            unpacked_IFPanoptionalheader_attributes[7], #demodfreqlow
            unpacked_IFPanoptionalheader_attributes[8], #demodfreqhigh
            unpacked_IFPanoptionalheader_attributes[9], #outputtimestamp
            unpacked_IFPanoptionalheader_attributes[10], #stepfreqnumerator
            unpacked_IFPanoptionalheader_attributes[11], #stepfreqdenom
            unpacked_IFPanoptionalheader_attributes[12], #signalsource
            unpacked_IFPanoptionalheader_attributes[13], #measuremode
            unpacked_IFPanoptionalheader_attributes[14], #measuretimestamp
            unpacked_IFPanoptionalheader_attributes[15], #selectivity
            unpacked_IFPanoptionalheader_attributes[16], #avgtype2
            unpacked_IFPanoptionalheader_attributes[17], #avgtype3
            unpacked_IFPanoptionalheader_attributes[18], #avgtype4
            unpacked_IFPanoptionalheader_attributes[19], #spmenabled
            unpacked_IFPanoptionalheader_attributes[20], #gateenabled
            unpacked_IFPanoptionalheader_attributes[21], #interval
            unpacked_IFPanoptionalheader_attributes[22], #gateoffset
            unpacked_IFPanoptionalheader_attributes[23], #gatelength
            unpacked_IFPanoptionalheader_attributes[24], #fEdge
            unpacked_IFPanoptionalheader_attributes[25], #traceID
        )
        return IFPanoptionalheadinstance
    return None
def EB200headerprint(datagram):
    print(f"Magic Number: {hex(datagram.magic_number)}")
    print(f"Version Major: {hex(datagram.version_major)}")
    print(f"Version Minor: {hex(datagram.version_minor)}")
    print(f"Sequence Number: {hex(datagram.sequence_number)}")
    print(f"Sequence Number High: {hex(datagram.seq_number_high)}")
    print(f"Attributes: {datagram.attributes}")
    print(f"Data Size: {datagram.data_size}")
    print(f"Length: {datagram.length}")
    print(f"Number of Trace Values: {datagram.number_of_trace_values}")
    print(f"Channel Number: {datagram.channel_number}")
    print(f"Optional Header Length: {datagram.optional_header_length}")
    print(f"Selector Flags: {datagram.selector_flags}")
    print("--------------")

@app.callback(
    [Output('x', 'data'), Output('y', 'data'),Output('min_data','data'), Output('max_data','data'),
     Output('time','data'), Output('initial_index','data'), Output('text','data'), Output('micro_symbol','data'),
     Output('updated_data','data')],

    [Input('upload-data', 'contents')]
)

def process_uploaded_file(decoded1):
    if decoded1 is None:
        return None, None,None,None,None,None,None,None,None
    content_type, content_string = decoded1.split(',')

    decoded1 = base64.b64decode(content_string)
    print(type(decoded1))
    # print(decoded1)
    print(len(content_type))
    print(len(content_string))
    index = 0
    pattern = b'\x00\x0e\xb2\x00'  # Byte pattern "000xEB200" in hexadecimal, seraches it
    pattern_length = len(pattern)
    datagram_list = []
    datagram_indexes = []
    channel_data = []
    channel_data2 = []
    channel_data3 = []
    channel_data4 = []
    while index < len(decoded1):
        index = decoded1.find(pattern, index)
        if index == -1:
            break

        if index + 16 <= len(decoded1):
            extracted_bytes = decoded1[index:index + 16]
            unpacked_data = struct.unpack('>I H H H H I', extracted_bytes)
            magic_number, version_minor, version_major, sequence_number, seq_number_high, data_size = unpacked_data
            next_2_bytes = decoded1[index + 16:index + 16 + 2]
            tagvalue = struct.unpack('>H', next_2_bytes)
            tag_value = tagvalue[0]  # get tag value
            reserved = struct.unpack('>H', decoded1[index + 16 + 2:index + 16 + 2 + 2])[0]
            length = struct.unpack('>I', decoded1[index + 16 + 2 + 2:index + 16 + 2 + 2 + 4])[0]
            reserved2 = struct.unpack('>4I', decoded1[index + 16 + 2 + 2 + 4:index + 16 + 2 + 2 + 4 + 16])[0]
            numberoftracevalues = \
            struct.unpack('>I', decoded1[index + 16 + 2 + 2 + 4 + 16:index + 16 + 2 + 2 + 4 + 16 + 4])[0]

            user_data = decoded1[index + 16 + 2 + 2 + 4:index + 16 + 2 + 2 + 4 + length]
            channelnumber = struct.unpack('>I', decoded1[index + 16 + 2 + 2 + 4 + 16 + 4:index + 16 + 2 + 2 + 4 + 16 + 4 + 4])[0]
            optionalheaderlength = struct.unpack('>I', decoded1[
                                                       index + 16 + 2 + 2 + 4 + 16 + 4 + 4:index + 16 + 2 + 2 + 4 + 16 + 4 + 4 + 4])[
                0]
            selectorflagslow = struct.unpack('>I', decoded1[
                                                   index + 16 + 2 + 2 + 4 + 16 + 4 + 4 + 4:index + 16 + 2 + 2 + 4 + 16 + 4 + 4 + 4 + 4])[
                0]
            selectorflagshigh = struct.unpack('>I', decoded1[
                                                    index + 16 + 2 + 2 + 4 + 16 + 4 + 4 + 4 + 4:index + 16 + 2 + 2 + 4 + 16 + 4 + 4 + 4 + 4 + 4])[
                0]

            datagram = EB200header1(
                magic_number,
                version_minor,
                version_major,
                sequence_number,
                seq_number_high,
                data_size,
                tag_value,
                reserved,
                length,
                reserved2,
                user_data,
                numberoftracevalues,
                channelnumber,
                optionalheaderlength,
                selectorflagslow,
                selectorflagshigh,
            )
            IFPANinstance = IFPANoptionalheaderprint(tag_value,decoded1,index)  # 10501
            if IFPANinstance is not None:
                IFPANLIST.append(IFPANinstance)
            num_indexes = len(IFPANLIST)

            if tag_value == 10501:  # if it is IFPAN datagram
                # Store the datagram and its index in the lists
                # manual parsing as certain parameters required
                freq_low = struct.unpack('<I', decoded1[index + 18 + 22 + 36:index + 18 + 22 + 36 + 4])
                freq_span = struct.unpack('<I', decoded1[index + 18 + 22 + 36 + 4:index + 18 + 22 + 36 + 4 + 4])
                measurementtimestamp = struct.unpack('<Q',
                                                     decoded1[index + 18 + 22 + 36 + 52:index + 18 + 22 + 36 + 60])
                measurementtimestamp = measurementtimestamp[0]
                measurementtimestamp = convert_unix_epoch(measurementtimestamp)
                timestampdata.append(measurementtimestamp)

                datagram_list.append(datagram)
                datagram_indexes.append(index)  # number of IFPAN datagrams

                # Update the index to search for the next occurrence of the pattern
                format_string = f'<{numberoftracevalues}h'

                channel_data_size = numberoftracevalues * 2  # Assuming each value is 2 bytes (INT16)

                if index + 184 + channel_data_size <= len(decoded1):
                    channel_values = struct.unpack(format_string, decoded1[
                                                                  index + 184:index + 184 + channel_data_size])

                    channel_data.append(channel_values)
                else:
                    print("Not enough data to unpack channel data.")

                if index + 184 + channel_data_size + channel_data_size <= len(decoded1):
                    channel_values1 = struct.unpack(format_string, decoded1[
                                                                   index + 184 + channel_data_size: index + 184 + channel_data_size + channel_data_size])

                    channel_data2.append(channel_values1)
                else:
                    print("Not enough data to unpack channel data.")

                if index + 184 + 2 * channel_data_size + channel_data_size <= len(decoded1):
                    channel_values = struct.unpack(format_string, decoded1[
                                                                  index + 184 + 2 * channel_data_size:index + 184 + 2 * channel_data_size + channel_data_size])

                    channel_data3.append(channel_values)
                else:
                    print("Not enough data to unpack channel data.")

                if index + 184 + 3 * channel_data_size + channel_data_size <= len(decoded1):
                    channel_values = struct.unpack(format_string, decoded1[
                                                                  index + 184 + 3 * channel_data_size:index + 184 + 3 * channel_data_size + channel_data_size])

                    channel_data4.append(channel_values)
                else:
                    print("Not enough data to unpack channel data.")

        # Now, unpack additional data following IFPAN
        # Define the format string for the additional data (adjust as needed)

        index += 1

    # Now you can access the stored datagrams by their indexes
    for i, index in enumerate(datagram_indexes):
        print(f"Datagram at index {i}: {datagram_list[i]}")
    number_of_indexes = len(datagram_list)

    #
    # def format_frequency(value, pos):
    #     return f'{value / 1e6:} '

    if channel_data:
        print("Channel Data:")
        for i, values in enumerate(channel_data):
            print(f"IFPAN  1_ {i + 1}:{values}")
            data.append(values)

    # if channel_data:
    #     print("Channel Data:")
    #     for i, values in enumerate(channel_data2):
    #         print(f"IFPAN  2_ {i + 1}:{values}")
    #         data2.append(values)
    # if channel_data:
    #     print("Channel Data:")
    #     for i, values in enumerate(channel_data3):
    #         print(f"IFPAN  3_ {i + 1}:{values}")
    #         data3.append(values)
    # if channel_data:
    #     print("Channel Data:")
    #     for i, values in enumerate(channel_data4):
    #         print(f"IFPAN  4_ {i + 1}:{values}")
    #         data4.append(values)

    # modify data
    updated_data = []
    for index in range(len(data)):
        updated_index = tuple(value / 10 for value in data[index])
        updated_data.append(updated_index)
    micro_symbol = '\u00B5'
    # print(updated)
    freq_low = freq_low[0]
    freq_low = freq_low / 10 ** 6
    freq_span = freq_span[0]
    freq_span = freq_span / 10 ** 6

    lower_frequency = freq_low - freq_span / 2
    step_size = freq_span / numberoftracevalues
    x = [(i * step_size) + lower_frequency for i in range(len(updated_data[i]))]

    # Initial index
    first_timestamp = datetime.datetime.strptime(timestampdata[0], '%Y-%m-%d %H:%M:%S')
    last_timestamp = datetime.datetime.strptime(timestampdata[-1], '%Y-%m-%d %H:%M:%S')

    # Calculate the time difference
    time_difference = last_timestamp - first_timestamp

    # Print the total time taken (in seconds)
    y = updated_data[index]
    # Initial index
    first_timestamp = datetime.datetime.strptime(timestampdata[0], '%Y-%m-%d %H:%M:%S')
    last_timestamp = datetime.datetime.strptime(timestampdata[-1], '%Y-%m-%d %H:%M:%S')

    # Calculate the time difference
    time_difference = last_timestamp - first_timestamp

    time = f"time taken: {time_difference.total_seconds()} seconds"
    initial_index = 0
    micro_symbol = '\u00B5'
    text = f"Timestamp: {timestampdata[index]}"
    all_data = [y for data in updated_data for y in data]
    min_data = int(np.floor(min(all_data)))  # Round down to nearest integer
    max_data = int(np.ceil(max(all_data)))  # Round up to nearest integer

    return x, y, min_data, max_data, time, initial_index, text, micro_symbol, updated_data


@app.callback(Output('index-slider', 'max'),
              [Input('updated_data', 'data')])
def update_slider_example_max(updated_data):
    if updated_data is None:
        return 0
    max_value = len(updated_data)-1
    return max_value

@app.callback(Output('threshold-slider', 'value'),
              [Input('min_data','data'),
               Input('max_data', 'data')])
def update_slider_example_value(min_data,max_data):
    if min_data or max_data is not None:
        min_value = min_data
        max_value = max_data
        value = (min_data+max_data)/2
        return value
    else: return 0

@app.callback(Output('threshold-slider', 'max'),
              [Input('max_data', 'data')])
def update_slider_example_max(max_data):
    max_value = max_data
    return max_value

# Callback to update the plot based on sliders
@app.callback(
    [Output('plot', 'figure'), Output('bandwidth-table', 'data'), Output('index-display', 'children'),Output('signal-alert', 'children')],
    [Input('index-slider', 'value'), Input('threshold-slider', 'value'), Input('toggle-y-axis', 'value'),  Input('x', 'data'), Input('y', 'data'), Input('min_data', 'data'), Input('max_data', 'data'),
     Input('time', 'data'), Input('initial_index', 'data'), Input('text', 'data'), Input('micro_symbol', 'data'),Input('updated_data', 'data')]
)

def update_plot(selected_index, threshold, toggle_value,x , y, min_data,max_data,time,initial_index,text,micro_symbol,updated_data):
    if updated_data is None:
        return go.Figure(),None,None,None
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=updated_data[selected_index], mode='lines+markers', name='Data'))
    index_display = html.Div(f"Selected Index: {selected_index}", style={'margin-top': '10px', 'font-weight': 'bold'})


    # Draw a red line at the threshold on the y-axis
    fig.add_shape(
        type='line',
        x0=min(x),
        y0=threshold,
        x1=max(x),
        y1=threshold,
        line=dict(color='red', width=2, dash='dash'),
    )

    # Highlight points above the threshold in red
    above_threshold_x = [x[i] for i, y in enumerate(updated_data[selected_index]) if y > threshold]
    above_threshold_y = [y for y in updated_data[selected_index] if y > threshold]
    fig.add_trace(go.Scatter(x=above_threshold_x, y=above_threshold_y, mode='markers', marker=dict(color='red'),
                             name='Above Threshold'))

    # Identify individual signals based on index proximity
    bandwidth_data =[]
    signals = []
    bandwidths = []
    colors = ['blue', 'green', 'orange', 'purple', 'cyan', 'red', 'yellow', 'pink', 'brown', 'teal', 'lavender', 'maroon', 'olive', 'navy', 'gold']   # Define colors for signals (add more if needed)
    color_idx = 0

    if len(above_threshold_x) > 0:
        signal = [above_threshold_x[0]]
        for i in range(1, len(above_threshold_x)):
            if above_threshold_x[i] - above_threshold_x[i - 1] <= 0.2:  # Adjust the threshold for signal closeness
                signal.append(above_threshold_x[i])
            else:
                signals.append(signal)
                signal = [above_threshold_x[i]]

        signals.append(signal)

        # Calculate bandwidth for each identified signal and highlight on the plot
        for signal in signals:
            if len(signal) > 1:
                signal_bandwidth = signal[-1] - signal[0]
                bandwidths.append(signal_bandwidth)

                # Highlight signal on the plot
                fig.add_trace(go.Scatter(
                    x=signal,
                    y=[threshold] * len(signal),
                    mode='markers',
                    marker=dict(color=colors[color_idx]),
                    name=f'Signal {color_idx + 1}'
                ))
                color_idx = (color_idx + 1) % len(colors)

    print("Bandwidths of identified signals:", bandwidths)
    for idx, signal in enumerate(signals):
        if len(signal) > 1:
            signal_bandwidth = signal[-1] - signal[0]
            bandwidths.append(signal_bandwidth)

            start_freq = signal[0]  # Start frequency of the signal
            end_freq = signal[-1]  # End frequency of the signal
            mean_freq = sum(signal) / len(signal)  # Mean frequency of the signal
            signal_points = []
            for i, x_val in enumerate(x):
                if x_val in signal:
                    signal_points.append((x_val, updated_data[int(selected_index)][i]))  # Collect x, y coordinates

            middle_point = None
            middle_point_index = None
            if signal_points:
                signal_points.sort()  # Sort the points by x value
                middle_point_index = len(signal_points) // 2  # Get the middle index
                middle_point = signal_points[middle_point_index][1]  # Extract the y-value of the middle point

            # Add data for each signal to bandwidth_data
            fig.update_layout(
                title='IFPAN Data ',
                xaxis_title='Frequencies (MHz)',
                yaxis_title=f'Signal Strength (db{micro_symbol})',
                annotations=[
                    dict(
                        text=f"Timestamp: {timestampdata[selected_index]}",
                        x=0.02,
                        y=1,
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(size=10, color='red')
                    ),
                    dict(
                        text=f"Total {time}",
                        x=0.02,
                        y=0.95,
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(size=10, color='red')
                    )
                ]
            )

            bandwidth_data.append({
                'Signal': f'Signal {idx + 1}',
                'Bandwidth': f'{signal_bandwidth:.2f} MHz',
                'Start Frequency': f'{start_freq:.2f} MHz',
                'End Frequency': f'{end_freq:.2f} MHz',
                'Center Frequency': f'{mean_freq:.2f} MHz',
                'Median Signal Strength': f'{middle_point} dB{micro_symbol}'
            })

    count = len([y for y in updated_data[selected_index] if y > threshold])

    alert_message = dbc.Alert(f'There is/are {idx+1} identified signal/signals above the threshold with {count} data points above the threshold.', color='info',
                              dismissable=True) if count > 0 else None
    # Code to identify signals and calculate bandwidths (as described in previous interactions)

    # bandwidth_data = [{'signal': f'Signal {idx + 1}', 'bandwidth': f'{bandwidth:.2f} MHz'}
    #                   for idx, bandwidth in enumerate(bandwidths)]
    yaxis_settings = {}
    if 'fixed-y-axis' in toggle_value:
        yaxis_settings['fixedrange'] = True
    else:
        yaxis_settings['fixedrange'] = False

    if yaxis_settings.get('fixedrange'):
        yaxis_settings['range'] = [min_data, max_data]  # Define your custom range here

    fig.update_layout(yaxis=yaxis_settings)
    return fig, bandwidth_data, index_display, alert_message

if __name__ == '__main__':
    app.run_server(debug=True)


