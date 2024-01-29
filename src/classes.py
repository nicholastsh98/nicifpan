#used to store classes
import datetime
#EB200 header class
class EB200header:
    def __init__(self,magicnumber,versionminor,versionmajor,sequencenumberlow,sequencenumberhigh,datasize):
        self.MagicNumber = magicnumber
        self.VersionMinor = versionminor
        self.VersionMajor = versionmajor
        self.SequenceNumberLow = sequencenumberlow
        self.SequenceNumberHigh = sequencenumberhigh
        self.DataSize = datasize

class conventionalattribute:
    def __init__(self, length):
        self.Length = length


class advancedattribute:
    def __init__(self, reserved1,length,reserved2):
        self.Reserved1 = reserved1
        self.Length = length
        self.Reserved2 = reserved2

class EB200header1:
    def __init__(self, magic_number, version_minor, version_major, sequence_number, seq_number_high, data_size,
                 tag_value, reserved, length, reserved2, user_data, numberoftracevalues, channelnumber,
                 optionalheaderlength, selectorflagslow, selectorflagshigh):
        self.magic_number = magic_number
        self.version_minor = version_minor
        self.version_major = version_major
        self.sequence_number = sequence_number
        self.seq_number_high = seq_number_high
        self.data_size = data_size
        self.tag_value = tag_value
        self.reserved = reserved
        self.length = length
        self.reserved2 = reserved2
        self.user_data = user_data
        self.numberoftracevalues = numberoftracevalues
        self.channelnumber = channelnumber
        self.optionalheaderlength = optionalheaderlength
        self.selectorflagslow = selectorflagslow
        self.selectorflagshigh = selectorflagshigh

    def __str__(self):
        return f"Magic Number: {hex(self.magic_number)}, Version Minor: {self.version_minor}, " \
               f"Version Major: {self.version_major}, Sequence Number: {self.sequence_number}, " \
               f"Seq Number High: {self.seq_number_high}, Data Size: {self.data_size}\n" \
               f"Tag Value: {self.tag_value}\nReserved: {self.reserved}\nLength: {self.length}\nReserved: {self.reserved2}\n" \
               f"User Data: {self.user_data.hex()}\nNumber of Trace Values: {self.numberoftracevalues}\n" \
               f"Channel Number: {self.channelnumber}\nOptional Header Length: {self.optionalheaderlength}\n" \
               f"Selector Flags Low: {self.selectorflagslow}\nSelector Flags High: {self.selectorflagshigh}"


class GenericAttribute:
    def __init__(self, tag, reserved, length, user_data):
        self.tag = tag
        self.reserved = reserved
        self.length = length
        self.user_data = user_data

    def __str__(self):
        return f"Tag: {self.tag}\nReserved: {self.reserved}\nLength: {self.length}\nUser Data: {self.user_data.hex()}"


class IFPanheader:
    def __init__(self, freq_low, freq_span, avgtime, avgtype, measuretime, freq_high, demodfreqchannel, demodfreq_low, demodfreq_high, outputtimestamp, stepfreqnumerator, stepfreqdenominator, signalsource, measuremode, measuretimestamp, selectivity, avgtype2, avgtype3, avgtype4, spmenabled, gateheaderenabled, gateheaderinterval, gateoffset, gatelength,fedge,traceid):
        self.Freq_low = freq_low
        self.Freq_span = freq_span
        self.Avgtime = avgtime
        self.Avgtype = avgtype
        self.Measuretime = measuretime
        self.Freq_high = freq_high
        self.Demodfreqchannel = demodfreqchannel
        self.Demodfreq_low = demodfreq_low
        self.Demodfreq_high = demodfreq_high
        self.Outputtimestamp = outputtimestamp
        self.Stepfreqnumerator = stepfreqnumerator
        self.Stepfreqdenominator = stepfreqdenominator
        self.Signalsource = signalsource
        self.Measuremode = measuremode
        self.Measuretimestamp = measuretimestamp
        self.Selectivity = selectivity
        self.Avgtype2 = avgtype2
        self.Avgtype3 = avgtype3
        self.Avgtype4 = avgtype4
        self.Spmenabled = spmenabled
        self.Gateheaderenabled = gateheaderenabled
        self.Gateheaderinterval = gateheaderinterval
        self.Gateoffset = gateoffset
        self.Gatelength = gatelength
        self.FEdge= fedge
        self.TranceID=traceid


    def print(self):
        print("For IFPAN Optional Header:")
        print(f"Freq low: {self.Freq_low / 10 ** 6} MHz")
        print(f"Freq Span: {self.Freq_span / 10 ** 6} MHz")
        print(f"Avg Time: {self.Avgtime}")
        print(f"Measure time: {self.Measuretime}")
        print(f"Freq High : {self.Freq_high}")
        print(f"DemodFreqChannel: {self.Demodfreqchannel / 10 ** 6} MHz")
        print(f"DemodFreq_low: {self.Demodfreq_low / 10 ** 6} MHz")
        print(f"DemodFreq_high: {self.Demodfreq_high / 10 ** 6} MHz")
        print("Output Time Stamp :",convert_unix_epoch(self.Outputtimestamp))
        print(f"StepFreqNumerator : {self.Stepfreqnumerator}")
        print(f"StepFreqDenom : {self.Stepfreqdenominator}")
        print(f"Signal Source: {self.Signalsource}")
        print(f"Measure Mode: {self.Measuremode}")
        print("Measure Time Stamp :",convert_unix_epoch(self.Measuretimestamp))
        print(f"Selectivity: {self.Selectivity}")
        print(f"AvgType2: {self.Avgtype2}")
        print(f"AvgType3: {self.Avgtype3}")
        print(f"AvgType4: {self.Avgtype4}")
        print(f"spmEnabled: {self.Spmenabled}")
        print(f"Gate Header Enabled: {self.Gateheaderenabled}")
        print(f"Gate Repetition Interval: {self.Gateheaderinterval} ns")
        print(f"Gate Offset within Interval: {self.Gateoffset} ns")
        print(f"Gate Length: {self.Gatelength} ns")
        print(f"fEdge: {hex(self.FEdge)} ")
        print(f"TraceID:{hex(self.TranceID)} ")

class DFPANheader: #dfpan optional header
    def __init__(self, freqlow,freqhigh,freqspan,dfthresholdmode,dfthresholdvalue,dfbandwidth,stepwidth,dfmeasuretime,dfoption,compassheading,compassheadingtype,antennafactor,demodfreqchannel,demodfreq_low,demodfreq_high
                 ,outputtimestamp,valid,noofsatinview,latref,latdeg,latmin,lonref,londeg,lonmin,hdop,stepfreqnumerator,stepfreqdenominator,dfbandwidthhighres,level,azimuth,quality,elevation,omniphase
                 ,reserved,measuretimestamp):
        self.FreqLow = freqlow
        self.FreqHigh = freqhigh
        self.FreqSpan = freqspan
        self.DFThresholdMode = dfthresholdmode
        self.DFThresholdValue = dfthresholdvalue
        self.DFBandwidth = dfbandwidth
        self.StepWidth = stepwidth
        self.DFMeasureTime = dfmeasuretime
        self.DFOption = dfoption
        self.CompassHeading = compassheading
        self.CompassHeadingType = compassheadingtype
        self.AntennaFactor = antennafactor
        self.DemodFreqChannel = demodfreqchannel
        self.DemodFreq_low = demodfreq_low
        self.DemodFreq_high = demodfreq_high
        self.OutputTimeStamp = outputtimestamp
        self.Valid = valid
        self.NoOfSatInView = noofsatinview
        self.LatRef = latref
        self.LatDeg = latdeg
        self.LatMin = latmin
        self.LonRef = lonref
        self.LonDeg = londeg
        self.LonMin = lonmin
        self.HDOP = hdop
        self.StepFreqNumerator = stepfreqnumerator
        self.StepFreqDemoninator = stepfreqdenominator
        self.DFBandwidthHighRes = dfbandwidthhighres
        self.Level = level
        self.Azimuth = azimuth
        self.Quality = quality
        self.Elevation = elevation
        self.Omniphase = omniphase
        self.Reserved = reserved
        self.MeasureTimeStamp = measuretimestamp

    def print(self):
        print("For DFPAN Optional Header:")
        print(f"Freq Low : {self.FreqLow/10**6} MHz")  # freqlow
        print(f"Freq High: {self.FreqHigh/10**6} MHz")  # freqspan
        print(f"Freq Span: {self.FreqSpan/10**6} Mhz")
        print(f"DF Threshold Mode: {self.DFThresholdMode} Hz")
        print(f"DF Threshold Value: {self.DFThresholdVallue} Hz")
        print(f"DF Bandwidth: {self.DFBandwidth} Hz")
        print(f"Step Width: ,{self.StepWidth}")
        print(f"DF MeasureTime:{self.DFMeasureTime} microseconds ")
        print(f"DF Option:{self.DFOption}")
        print(f"Compass Heading:{self.CompassHeading} ")
        print(f"Compass Heading Type:{self.CompassHeadingType} ")
        print(f"Antenna Factor : {self.AntennaFactor}")
        print(f"Demod Frequency Channel : {self.DemodFreqChannel}")
        print(f"Demod Frequency Low : {self.DemodFreq_low}")
        print(f"Demod Frequency High : {self.DemodFreq_high}")
        print("Output Time Stamp: ", convert_unix_epoch(self.OutputTimestamp))
        print(f"Valid : {self.Valid}")  # freqlow
        print(f"No. of Satelites in View: {self.NoOfSatInView} ")  # freqspan
        print(f"Lattitude Direction: {self.LatRef}")
        print(f"Lattitude Degrees: {self.LatDeg}")
        print(f"Lattitude Geographical in minutes: {self.LatMin}")
        print(f"Longitude Direction: {self.LonRef}")
        print(f"Step Frequency Numerator:{self.StepFreqNumerator} ")
        print(f"Step Frequency Denominator:{self.StepFreqDemoninator} ")
        print(f"High resolution representation:{self.DFBandwidthHighRes} ")
        print(f"Level: {self.Level}")
        print(f"Azimuth: {self.Azimuth}")
        print(f"Quality: {self.Quality}")
        print(f"ELevation: {self.Elevation}")
        # print(": ", convert_unix_epoch(self.OutputTimestamp))
        print(f"Ominiphase:{self.Omniphase} ")
        print(f"Reserved:{self.Reserved} ")
        print("Measure Time Stamp: ", convert_unix_epoch(self.MeasureTimeStamp))


def convert_unix_epoch(value):
    # Create a datetime object from the timestamp in seconds
    timestamp_seconds = value // 10 ** 9
    timestamp_datetime = datetime.datetime.utcfromtimestamp(timestamp_seconds)

    # Format the datetime object as a human-readable string
    human_readable_format = timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')

    return human_readable_format
