# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km 
#  Text explaining script usage
# Parameters:
#  o_x_km: ground station
#  o_y_km:
#  o_z_km:
#  x_km: Satellite
#  y_km:
#  z_km:
#  ...
# Output:
#  A description of the script output
#
# Written by Nicola DeMarinis
# Other contributors: Brad Denby
#
# Optional license statement, e.g., See the LICENSE file for the license.

# import Python modules
# e.g., import math # math module
import math # math module
import sys  # argv
import numpy # matrix math

# "constants"
R_E_KM = 6378.1363
E_E    = 0.081819221456

# initialize script arguments
o_x_km = float('nan') # ECEF x-component of the ground station in km
o_y_km = float('nan') # ECEF y-component in km
o_z_km = float('nan') # ECEF z-component in km
x_km = float('nan') # ECEF x-component of the object in km
y_km = float('nan') # ECEF y-component in km
z_km = float('nan') # ECEF z-component in km

# parse script arguments
if len(sys.argv)==7:
  o_x_km = float(sys.argv[1])
  o_y_km = float(sys.argv[2])
  o_z_km = float(sys.argv[3])
  x_km = float(sys.argv[4])
  y_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
   'Usage: '\
   'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'\
  )
  exit()

# write script below this line

# calculate denominator
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

# calculate longitude
lon_rad = math.atan2(o_y_km,o_x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(o_z_km/math.sqrt(o_x_km**2+o_y_km**2+o_z_km**2))
r_lon_km = math.sqrt(o_x_km**2+o_y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((o_z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1
  
# calculate hae
hae_km = r_lon_km/math.cos(lat_rad)-c_E

#I now have lon_rad, lat_rad, hae_km of the observation site

ecef_x_km = x_km - o_x_km
ecef_y_km = y_km - o_y_km
ecef_z_km = z_km - o_z_km

s_km = -ecef_z_km*math.cos(lat_rad) + ecef_x_km*math.cos(lon_rad)*math.sin(lat_rad) + ecef_y_km*math.sin(lon_rad)*math.sin(lat_rad)
e_km = ecef_y_km*math.cos(lon_rad) - ecef_x_km*math.sin(lon_rad)
z_km = ecef_x_km*math.cos(lon_rad)*math.cos(lat_rad) + ecef_y_km*math.cos(lat_rad)*math.sin(lon_rad) + ecef_z_km*math.sin(lat_rad)

# Final Print Statments
print(s_km)
print(e_km)
print(z_km)