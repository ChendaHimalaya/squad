import os
import psutil
import time


def collect_metrics(filename):
    f = open(filename, "a")
    result = []
    # Output current CPU usage as a percentage
    result.append('{}'.format(get_cpu_usage_pct()))
    result.append('{}'.format(get_cpu_usage_pct_percpu()))
    # Output current CPU frequency in MHz.
    result.append('{}'.format(get_cpu_frequency()))
    # Output current CPU temperature in degrees Celsius
    result.append('{}'.format(get_cpu_temp()))
    # Output current RAM usage in MB
    result.append('{}'.format(int(get_ram_usage() / 1024 / 1024)))
    # Output total RAM in MB
    result.append('{}'.format(int(get_ram_total() / 1024 / 1024)))
    # Output current RAM usage as a percentage.
    result.append('{}'.format(get_ram_usage_pct()))
    # Output current Swap usage in MB
    result.append('{}'.format(int(get_swap_usage() / 1024 / 1024)))
    # Output total Swap in MB
    result.append('{}'.format(int(get_swap_total() / 1024 / 1024)))
    # Output current Swap usage as a percentage.
    result.append('{}'.format(get_swap_usage_pct()))
    f.write("|".join(result)+"\n")
    f.close()

def main():
    f = open("system_metrics.csv", "a")
    f.write("CPU usage|CPU usage percpu|CPU frequency|CPU temperature|RAM usage|RAM total|RAM usage percent|Swap usage|Swap total|Swap percent\n")
    f.close()
    while True:
        collect_metrics("system_metrics.csv")
        time.sleep(1)
    
    
def get_cpu_usage_pct():
    """
    Obtains the system's average CPU load as measured over a period of 500 milliseconds.
    :returns: System CPU load as a percentage.
    :rtype: float
    """
    return psutil.cpu_percent(interval=0.5)

def get_cpu_usage_pct_percpu():
    """
    Obtains the system's average CPU load as measured over a period of 500 milliseconds.
    :returns: System CPU load as a percentage.
    :rtype: float
    """
    return psutil.cpu_percent(interval=0.5, percpu = True)


def get_cpu_frequency():
    """
    Obtains the real-time value of the current CPU frequency.
    :returns: Current CPU frequency in MHz.
    :rtype: int
    """
    return int(psutil.cpu_freq().current)


def get_cpu_temp():
    """
    Obtains the current value of the CPU temperature.
    :returns: Current value of the CPU temperature if successful, zero value otherwise.
    :rtype: float
    """
    # Initialize the result.
    result = 0.0
    # The first line in this file holds the CPU temperature as an integer times 1000.
    # Read the first line and remove the newline character at the end of the string.
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()
        # Test if the string is an integer as expected.
        if line.isdigit():
            # Convert the string with the CPU temperature to a float in degrees Celsius.
            result = float(line) / 1000
    # Give the result back to the caller.
    return result


def get_ram_usage():
    """
    Obtains the absolute number of RAM bytes currently in use by the system.
    :returns: System RAM usage in bytes.
    :rtype: int
    """
    return int(psutil.virtual_memory().total - psutil.virtual_memory().available)


def get_ram_total():
    """
    Obtains the total amount of RAM in bytes available to the system.
    :returns: Total system RAM in bytes.
    :rtype: int
    """
    return int(psutil.virtual_memory().total)


def get_ram_usage_pct():
    """
    Obtains the system's current RAM usage.
    :returns: System RAM usage as a percentage.
    :rtype: float
    """
    return psutil.virtual_memory().percent


def get_swap_usage():
    """
    Obtains the absolute number of Swap bytes currently in use by the system.
    :returns: System Swap usage in bytes.
    :rtype: int
    """
    return int(psutil.swap_memory().used)


def get_swap_total():
    """
    Obtains the total amount of Swap in bytes available to the system.
    :returns: Total system Swap in bytes.
    :rtype: int
    """
    return int(psutil.swap_memory().total)


def get_swap_usage_pct():
    """
    Obtains the system's current Swap usage.
    :returns: System Swap usage as a percentage.
    :rtype: float
    """
    return psutil.swap_memory().percent

print("je;l")
main()