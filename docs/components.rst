

Here are some generic Parametric cells.

You can customize them your fab or use them as an inspiration to build your own.


Parametric cells
=============================


C
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.C

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.C(width=1.0, size=[10.0, 20.0], layer='WG')
  c.plot_matplotlib()



L
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.L

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.L(width=1, size=[10, 20], layer='M3', port_type='electrical')
  c.plot_matplotlib()



add_fiducials
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.add_fiducials

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.add_fiducials(gap=50, left='cross', right='cross', offset=[0, 0])
  c.plot_matplotlib()



add_fiducials_offsets
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.add_fiducials_offsets

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.add_fiducials_offsets(fiducial='cross', offsets=[[0, 100], [0, -100]])
  c.plot_matplotlib()



add_frame
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.add_frame

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.add_frame(width=10.0, spacing=10.0, layer='WG')
  c.plot_matplotlib()



add_grating_couplers
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.add_grating_couplers

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.add_grating_couplers(layer_label=[200, 0], gc_port_name='o1')
  c.plot_matplotlib()



add_grating_couplers_with_loopback_fiber_array
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.add_grating_couplers_with_loopback_fiber_array

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.add_grating_couplers_with_loopback_fiber_array(grating_separation=127.0, gc_port_name='o1', gc_rotation=-90, straight_separation=5.0, layer_label=[200, 0], with_loopback=False, nlabels_loopback=2, loopback_yspacing=4.0)
  c.plot_matplotlib()



add_grating_couplers_with_loopback_fiber_single
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.add_grating_couplers_with_loopback_fiber_single

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.add_grating_couplers_with_loopback_fiber_single(layer_label=[200, 0], gc_port_name='o1', with_loopback=True, loopback_xspacing=5.0, rotation=90)
  c.plot_matplotlib()



add_trenches
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.add_trenches

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.add_trenches(cross_section='rib_with_trenches', top=True, bot=True, right=False, left=False)
  c.plot_matplotlib()



add_trenches90
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.add_trenches90

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.add_trenches90(cross_section='rib_with_trenches', top=False, bot=True, right=True, left=False)
  c.plot_matplotlib()



align_wafer
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.align_wafer

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.align_wafer(width=10.0, spacing=10.0, cross_length=80.0, layer='WG', square_corner='bottom_left')
  c.plot_matplotlib()



array
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.array

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.array(spacing=[150.0, 150.0], columns=6, rows=1, add_ports=True)
  c.plot_matplotlib()



array_with_fanout
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.array_with_fanout

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.array_with_fanout(component='pad', columns=3, pitch=150.0, waveguide_pitch=10.0, start_straight_length=5.0, end_straight_length=40.0, radius=5.0, component_port_name='e4', bend='bend_euler', cross_section='strip')
  c.plot_matplotlib()



array_with_fanout_2d
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.array_with_fanout_2d

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.array_with_fanout_2d(pitch=150.0, columns=3, rows=2)
  c.plot_matplotlib()



array_with_via
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.array_with_via

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.array_with_via(columns=3, spacing=150.0, via_spacing=10.0, straight_length=60.0, via_stack_dy=0, port_angle=180)
  c.plot_matplotlib()



array_with_via_2d
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.array_with_via_2d

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.array_with_via_2d(spacing=[150.0, 150.0], columns=3, rows=2)
  c.plot_matplotlib()



awg
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.awg

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.awg(arms=10, outputs=3, fpr_spacing=50.0)
  c.plot_matplotlib()



bbox
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bbox

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bbox(bbox=[[-1.0, -1.0], [3.0, 4.0]], layer=[1, 0], top=0, bottom=0, left=0, right=0)
  c.plot_matplotlib()



bend_circular
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bend_circular

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bend_circular(angle=90.0, with_bbox=True, cross_section='strip')
  c.plot_matplotlib()



bend_circular180
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bend_circular180

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bend_circular180(angle=180, with_bbox=True, cross_section='strip')
  c.plot_matplotlib()



bend_circular_heater
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bend_circular_heater

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bend_circular_heater(radius=10, angle=90, heater_to_wg_distance=1.2, heater_width=0.5, layer_heater='HEATER', with_bbox=True, cross_section='strip')
  c.plot_matplotlib()



bend_euler
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bend_euler

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bend_euler(angle=90.0, p=0.5, with_arc_floorplan=True, direction='ccw', with_bbox=True, cross_section='strip')
  c.plot_matplotlib()



bend_euler180
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bend_euler180

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bend_euler180(angle=180, p=0.5, with_arc_floorplan=True, direction='ccw', with_bbox=True, cross_section='strip')
  c.plot_matplotlib()



bend_euler_s
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bend_euler_s

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bend_euler_s()
  c.plot_matplotlib()



bend_euler_trenches
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bend_euler_trenches

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bend_euler_trenches(cross_section='rib_with_trenches', top=False, bot=True, right=True, left=False)
  c.plot_matplotlib()



bend_port
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bend_port

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bend_port(port_name='e1', port_name2='e2', cross_section='metal3_with_bend', angle=180)
  c.plot_matplotlib()



bend_s
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bend_s

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bend_s(size=[11.0, 2.0], npoints=99, cross_section='strip', check_min_radius=False)
  c.plot_matplotlib()



bend_straight_bend
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bend_straight_bend

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bend_straight_bend(straight_length=10.0, angle=90, p=0.5, with_arc_floorplan=True, npoints=720, direction='ccw')
  c.plot_matplotlib()



bezier
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.bezier

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.bezier(control_points=[[0.0, 0.0], [5.0, 0.0], [5.0, 2.0], [10.0, 2.0]], npoints=201, with_manhattan_facing_angles=True, cross_section='strip', with_bbox=True)
  c.plot_matplotlib()



cavity
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cavity

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cavity(coupler='coupler', length=0.1, gap=0.2)
  c.plot_matplotlib()



cdc
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cdc

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cdc(length=30.0, gap=0.5, period=0.22, dc=0.5, dx=10.0, dy=5.0, width_top=2.0, width_bot=0.75, fins=False, fin_size=[0.2, 0.05])
  c.plot_matplotlib()



cdsem_all
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cdsem_all

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cdsem_all(widths=[0.4, 0.45, 0.5, 0.6, 0.8, 1.0], dense_lines_width=0.3, dense_lines_width_difference=0.02, dense_lines_gap=0.3, dense_lines_labels=['DL', 'DM', 'DH'], straight='straight', bend90='bend_circular', cross_section='strip')
  c.plot_matplotlib()



circle
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.circle

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.circle(radius=10.0, angle_resolution=2.5, layer='WG')
  c.plot_matplotlib()



coh_rx_dual_pol
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coh_rx_dual_pol

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coh_rx_dual_pol(cross_section='strip', lo_splitter='mmi1x2', single_pol_rx_spacing=50.0, splitter_coh_rx_spacing=40.0)
  c.plot_matplotlib()



coh_rx_single_pol
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coh_rx_single_pol

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coh_rx_single_pol(bend='bend_euler', cross_section='strip', det_spacing=[60.0, 50.0], with_pads=True, pad_det_spacing=80.0, in_wg_length=20.0)
  c.plot_matplotlib()



coh_tx_dual_pol
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coh_tx_dual_pol

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coh_tx_dual_pol(splitter='mmi1x2', spol_coh_tx='coh_tx_single_pol', yspacing=10.0, xspacing=40.0, cross_section='strip')
  c.plot_matplotlib()



coh_tx_single_pol
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coh_tx_single_pol

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coh_tx_single_pol(balanced_phase_shifters=False, mzm_y_spacing=50.0, phase_shifter='straight_pin', phase_shifter_length=100.0, mzm_ps_spacing=40.0, splitter='mmi1x2', mzm_length=200.0, with_pads=False, xspacing=40.0, pad_array='pad_array', cross_section='strip')
  c.plot_matplotlib()



compass
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.compass

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.compass(size=[4.0, 2.0], layer='WG', port_type='placement', port_inclusion=0.0, port_angles=[180, 90, 0, -90])
  c.plot_matplotlib()



compensation_path
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.compensation_path

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.compensation_path(direction='top', cross_section='strip')
  c.plot_matplotlib()



component_lattice
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.component_lattice



component_sequence
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.component_sequence



copy_layers
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.copy_layers

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.copy_layers(layers=[[1, 0], [2, 0]])
  c.plot_matplotlib()



coupler
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler(gap=0.236, length=20.0, dy=4.0, dx=10.0, cross_section='strip')
  c.plot_matplotlib()



coupler90
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler90

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler90(gap=0.2, radius=10.0, cross_section='strip')
  c.plot_matplotlib()



coupler90bend
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler90bend

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler90bend(radius=10.0, gap=0.2, cross_section_inner='strip', cross_section_outer='strip')
  c.plot_matplotlib()



coupler90circular
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler90circular

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler90circular(gap=0.2, radius=10.0, cross_section='strip')
  c.plot_matplotlib()



coupler_adiabatic
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler_adiabatic

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler_adiabatic(length1=20.0, length2=50.0, length3=30.0, wg_sep=1.0, input_wg_sep=3.0, output_wg_sep=3.0, dw=0.1, cross_section='strip')
  c.plot_matplotlib()



coupler_asymmetric
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler_asymmetric

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler_asymmetric(gap=0.234, dy=5.0, dx=10.0, cross_section='strip')
  c.plot_matplotlib()



coupler_bend
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler_bend

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler_bend(radius=10.0, coupler_gap=0.2, coupling_angle_coverage=120.0, cross_section_inner='strip', cross_section_outer='strip')
  c.plot_matplotlib()



coupler_full
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler_full

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler_full(coupling_length=40.0, dx=10.0, dy=5.0, gap=0.5, dw=0.1, cross_section='strip')
  c.plot_matplotlib()



coupler_ring
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler_ring

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler_ring(gap=0.2, radius=5.0, length_x=4.0, cross_section='strip', length_extension=3)
  c.plot_matplotlib()



coupler_straight
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler_straight

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler_straight(length=10.0, gap=0.27)
  c.plot_matplotlib()



coupler_straight_asymmetric
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler_straight_asymmetric

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler_straight_asymmetric(length=10.0, gap=0.27, width_top=0.5, width_bot=1)
  c.plot_matplotlib()



coupler_symmetric
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler_symmetric

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler_symmetric(gap=0.234, dy=5.0, dx=10.0, cross_section='strip')
  c.plot_matplotlib()



coupler_trenches
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.coupler_trenches

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.coupler_trenches(cross_section='rib_with_trenches', top=True, bot=True, right=False, left=False)
  c.plot_matplotlib()



cross
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cross

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cross(length=10.0, width=3.0, layer='WG')
  c.plot_matplotlib()



crossing
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.crossing

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.crossing(cross_section='strip')
  c.plot_matplotlib()



crossing45
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.crossing45

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.crossing45(port_spacing=40.0, alpha=0.08, npoints=101, cross_section='strip')
  c.plot_matplotlib()



crossing_arm
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.crossing_arm

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.crossing_arm(r1=3.0, r2=1.1, w=1.2, L=3.4, layer_slab='SLAB150', cross_section='strip')
  c.plot_matplotlib()



crossing_etched
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.crossing_etched

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.crossing_etched(width=0.5, r1=3.0, r2=1.1, w=1.2, L=3.4, layer_wg='WG', layer_slab='SLAB150')
  c.plot_matplotlib()



crossing_from_taper
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.crossing_from_taper

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.crossing_from_taper()
  c.plot_matplotlib()



cutback_2x2
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cutback_2x2

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cutback_2x2(cols=4, rows=5, port1='o1', port2='o2', port3='o3', port4='o4', mirror=False, cross_section='strip')
  c.plot_matplotlib()



cutback_bend
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cutback_bend

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cutback_bend(straight_length=5.0, rows=6, columns=5)
  c.plot_matplotlib()



cutback_bend180
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cutback_bend180

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cutback_bend180(straight_length=5.0, rows=6, columns=6, spacing=3)
  c.plot_matplotlib()



cutback_bend180circular
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cutback_bend180circular

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cutback_bend180circular(straight_length=5.0, rows=6, columns=6, spacing=3)
  c.plot_matplotlib()



cutback_bend90
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cutback_bend90

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cutback_bend90(straight_length=5.0, rows=6, columns=6, spacing=5)
  c.plot_matplotlib()



cutback_bend90circular
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cutback_bend90circular

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cutback_bend90circular(straight_length=5.0, rows=6, columns=6, spacing=5)
  c.plot_matplotlib()



cutback_component
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cutback_component

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cutback_component(cols=4, rows=5, port1='o1', port2='o2', mirror=False, mirror1=False, mirror2=False, cross_section='strip')
  c.plot_matplotlib()



cutback_component_mirror
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cutback_component_mirror

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cutback_component_mirror(cols=4, rows=5, port1='o1', port2='o2', mirror=True, mirror1=False, mirror2=False, cross_section='strip')
  c.plot_matplotlib()



cutback_splitter
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.cutback_splitter

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.cutback_splitter(cols=4, rows=5, port1='o1', port2='o2', port3='o3', mirror=False, cross_section='strip')
  c.plot_matplotlib()



dbr
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.dbr

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.dbr(w1=0.475, w2=0.525, l1=0.159, l2=0.159, n=10, cross_section='strip')
  c.plot_matplotlib()



dbr_tapered
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.dbr_tapered

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.dbr_tapered(length=10.0, period=0.85, dc=0.5, w1=0.4, w2=1.0, taper_length=20.0, fins=False, fin_size=[0.2, 0.05], cross_section='strip')
  c.plot_matplotlib()



delay_snake
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.delay_snake

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.delay_snake(length=1600.0, L0=5.0, n=2, bend='bend_euler', cross_section='strip')
  c.plot_matplotlib()



delay_snake2
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.delay_snake2

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.delay_snake2(length=1600.0, length0=0.0, length2=0.0, n=2, bend180='bend_euler180', cross_section='strip')
  c.plot_matplotlib()



delay_snake3
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.delay_snake3

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.delay_snake3(length=1600.0, length0=0.0, length2=0.0, n=2, cross_section='strip')
  c.plot_matplotlib()



delay_snake_sbend
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.delay_snake_sbend

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.delay_snake_sbend(length=100.0, length1=0.0, length4=0.0, radius=5.0, waveguide_spacing=5.0, bend='bend_euler', sbend='bend_s', sbend_xsize=100.0, cross_section='strip')
  c.plot_matplotlib()



dicing_lane
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.dicing_lane

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.dicing_lane(size=[50, 300], layer_dicing='DICING')
  c.plot_matplotlib()



die
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.die

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.die(size=[10000.0, 10000.0], street_width=100.0, street_length=1000.0, die_name='chip99', text_size=100.0, text_location='SW', layer='FLOORPLAN', bbox_layer='FLOORPLAN', draw_corners=True, draw_dicing_lane=True)
  c.plot_matplotlib()



die_bbox
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.die_bbox

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.die_bbox(street_width=100.0, text_size=100.0, text_anchor='sw', layer='M3', padding=10.0)
  c.plot_matplotlib()



die_bbox_frame
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.die_bbox_frame

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.die_bbox_frame(bbox=[[-1.0, -1.0], [3.0, 4.0]], street_width=100.0, street_length=1000.0, text_size=100.0, text_anchor='sw', layer='M3', padding=10.0)
  c.plot_matplotlib()



disk
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.disk

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.disk(radius=10.0, gap=0.2, wrap_angle_deg=180.0, parity=1, cross_section='strip')
  c.plot_matplotlib()



disk_heater
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.disk_heater

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.disk_heater(radius=10.0, gap=0.2, wrap_angle_deg=180.0, parity=1, cross_section='strip', heater_layer='HEATER', via_stack='via_stack_heater_mtop', heater_width=5.0, heater_extent=2.0, via_width=10.0, port_angle=90)
  c.plot_matplotlib()



edge_coupler_array
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.edge_coupler_array

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.edge_coupler_array(n=5, pitch=127.0, x_reflection=False, text_offset=[10, 20], text_rotation=0)
  c.plot_matplotlib()



edge_coupler_array_with_loopback
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.edge_coupler_array_with_loopback

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.edge_coupler_array_with_loopback(cross_section='strip', radius=30, n=8, pitch=127.0, extension_length=1.0, right_loopback=True, x_reflection=False, text_offset=[0, 0], text_rotation=0)
  c.plot_matplotlib()



edge_coupler_silicon
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.edge_coupler_silicon

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.edge_coupler_silicon(length=100, width1=0.5, width2=0.2, with_bbox=True, with_two_ports=False, cross_section='strip')
  c.plot_matplotlib()



ellipse
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ellipse

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ellipse(radii=[10.0, 5.0], angle_resolution=2.5, layer='WG')
  c.plot_matplotlib()



extend_port
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.extend_port



extend_ports
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.extend_ports

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.extend_ports(length=5.0, port_type='optical', centered=False)
  c.plot_matplotlib()



extend_ports_list
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.extend_ports_list



fiber
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.fiber

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.fiber(core_diameter=10, cladding_diameter=125, layer_core='WG', layer_cladding='WGCLAD')
  c.plot_matplotlib()



fiber_array
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.fiber_array

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.fiber_array(n=8, pitch=127.0, core_diameter=10, cladding_diameter=125, layer_core='WG', layer_cladding='WGCLAD')
  c.plot_matplotlib()



fiducial_squares
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.fiducial_squares

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.fiducial_squares(layers=[[1, 0]], size=[5, 5], offset=0.14)
  c.plot_matplotlib()



ge_detector_straight_si_contacts
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ge_detector_straight_si_contacts

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ge_detector_straight_si_contacts(length=80.0, via_stack_width=10.0, via_stack_spacing=5.0, via_stack_offset=0.0)
  c.plot_matplotlib()



grating_coupler_array
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_array

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_array(pitch=127.0, n=6, port_name='o1', rotation=0)
  c.plot_matplotlib()



grating_coupler_dual_pol
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_dual_pol

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_dual_pol(period_x=0.58, period_y=0.58, x_span=11, y_span=11, length_taper=150.0, width_taper=10.0, polarization='dual', wavelength=1.55, base_layer='WG', cross_section='strip')
  c.plot_matplotlib()



grating_coupler_elliptical
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_elliptical

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_elliptical(polarization='te', taper_length=16.6, taper_angle=40.0, wavelength=1.554, fiber_angle=15.0, grating_line_width=0.343, neff=2.638, nclad=1.443, n_periods=30, big_last_tooth=False, layer_slab='SLAB150', slab_xmin=-1.0, slab_offset=2.0, spiked=True, cross_section='strip')
  c.plot_matplotlib()



grating_coupler_elliptical_arbitrary
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_elliptical_arbitrary

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_elliptical_arbitrary(gaps=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1], widths=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], taper_length=16.6, taper_angle=60.0, wavelength=1.554, fiber_angle=15.0, nclad=1.443, layer_slab='SLAB150', taper_to_slab_offset=-3.0, polarization='te', spiked=True, bias_gap=0, cross_section='strip')
  c.plot_matplotlib()



grating_coupler_elliptical_lumerical
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_elliptical_lumerical

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_elliptical_lumerical(parameters=[-2.4298362615732447, 0.1, 0.48007023217536954, 0.1, 0.607397685752365, 0.1, 0.4498844003086115, 0.1, 0.4274116312627637, 0.1, 0.4757904248387285, 0.1, 0.5026649898504233, 0.10002922416240886, 0.5100366774007897, 0.1, 0.494399635363353, 0.1079599958465788, 0.47400592737426483, 0.14972685326277918, 0.43272750134545823, 0.1839530796530385, 0.3872023336708212, 0.2360175325711591, 0.36032212454768675, 0.24261846353500535, 0.35770350120764394, 0.2606637836858316, 0.3526104381544335, 0.24668202254540886, 0.3717488388788273, 0.22920754299702897, 0.37769616507688464, 0.2246528336925301, 0.3765437598650894, 0.22041773376471022, 0.38047596041838994, 0.21923601658169187, 0.3798873698864591, 0.21700438236445285, 0.38291698672245644, 0.21827768053295463, 0.3641322152037017, 0.23729077006065105, 0.3676834419346081, 0.24865079519725933, 0.34415050295044936, 0.2733570818755685, 0.3306230780901629, 0.27350446437732157], layer='WG', layer_slab='SLAB150', taper_angle=55, taper_length=12.6, fiber_angle=5, bias_gap=0)
  c.plot_matplotlib()



grating_coupler_elliptical_te
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_elliptical_te

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_elliptical_te(polarization='te', taper_length=16.6, taper_angle=40.0, wavelength=1.554, fiber_angle=15.0, grating_line_width=0.343, neff=2.638, nclad=1.443, n_periods=30, big_last_tooth=False, layer_slab='SLAB150', slab_xmin=-1.0, slab_offset=2.0, spiked=True, cross_section='strip')
  c.plot_matplotlib()



grating_coupler_elliptical_tm
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_elliptical_tm

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_elliptical_tm(polarization='tm', taper_length=30, taper_angle=40.0, wavelength=1.554, fiber_angle=15.0, grating_line_width=0.707, neff=1.8, nclad=1.443, n_periods=16, big_last_tooth=False, layer_slab='SLAB150', slab_xmin=-2, slab_offset=2.0, spiked=True, cross_section='strip')
  c.plot_matplotlib()



grating_coupler_elliptical_trenches
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_elliptical_trenches

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_elliptical_trenches(polarization='te', taper_length=16.6, taper_angle=30.0, trenches_extra_angle=9.0, wavelength=1.53, fiber_angle=15.0, grating_line_width=0.343, neff=2.638, ncladding=1.443, layer_trench='SHALLOW_ETCH', p_start=26, n_periods=30, end_straight_length=0.2, cross_section='strip')
  c.plot_matplotlib()



grating_coupler_elliptical_uniform
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_elliptical_uniform

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_elliptical_uniform(n_periods=20, period=0.75, fill_factor=0.5)
  c.plot_matplotlib()



grating_coupler_loss_fiber_array
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_loss_fiber_array

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_loss_fiber_array(pitch=127.0, input_port_indexes=[0, 1])
  c.plot_matplotlib()



grating_coupler_loss_fiber_array4
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_loss_fiber_array4

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_loss_fiber_array4(pitch=127.0)
  c.plot_matplotlib()



grating_coupler_loss_fiber_single
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_loss_fiber_single

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_loss_fiber_single(cross_section='strip')
  c.plot_matplotlib()



grating_coupler_rectangular
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_rectangular

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_rectangular(n_periods=20, period=0.75, fill_factor=0.5, width_grating=11.0, length_taper=150.0, polarization='te', wavelength=1.55, layer_slab='SLAB150', fiber_angle=15, slab_xmin=-1.0, slab_offset=1.0, cross_section='strip')
  c.plot_matplotlib()



grating_coupler_rectangular_arbitrary
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_rectangular_arbitrary

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_rectangular_arbitrary(gaps=[0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2], widths=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], width_grating=11.0, length_taper=150.0, polarization='te', wavelength=1.55, layer_slab='SLAB150', slab_xmin=-1.0, slab_offset=1.0, fiber_angle=15, cross_section='strip')
  c.plot_matplotlib()



grating_coupler_rectangular_arbitrary_slab
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_rectangular_arbitrary_slab

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_rectangular_arbitrary_slab(gaps=[0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2], widths=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5], width_grating=11.0, length_taper=150.0, polarization='te', wavelength=1.55, layer_slab='SLAB150', slab_offset=2.0, fiber_angle=15, cross_section='strip')
  c.plot_matplotlib()



grating_coupler_te
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_te

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_te(polarization='te', taper_length=16.6, taper_angle=35, trenches_extra_angle=9.0, wavelength=1.53, fiber_angle=15.0, grating_line_width=0.343, neff=2.638, ncladding=1.443, layer_trench='SHALLOW_ETCH', p_start=26, n_periods=30, end_straight_length=0.2, cross_section='strip')
  c.plot_matplotlib()



grating_coupler_tm
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_tm

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_tm(polarization='tm', taper_length=16.6, taper_angle=30.0, trenches_extra_angle=9.0, wavelength=1.53, fiber_angle=15.0, grating_line_width=0.6, neff=1.8, ncladding=1.443, layer_trench='SHALLOW_ETCH', p_start=26, n_periods=30, end_straight_length=0.2, cross_section='strip')
  c.plot_matplotlib()



grating_coupler_tree
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.grating_coupler_tree

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.grating_coupler_tree(n=4, straight_spacing=4.0, with_loopback=False, bend='bend_euler', fanout_length=0.0, layer_label='TEXT')
  c.plot_matplotlib()



greek_cross
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.greek_cross

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.greek_cross(length=30, layers=['WG', 'N'], widths=[2.0, 3.0])
  c.plot_matplotlib()



greek_cross_offset_pads
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.greek_cross_offset_pads

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.greek_cross_offset_pads(cross_struct_length=30.0, cross_struct_width=1.0, cross_struct_layers=['WG'], cross_implant_length=30.0, cross_implant_width=2.0, cross_implant_layers=['N'], contact_layers=['WG', 'NPP'], contact_offset=10, contact_buffer=10, pad_width=50)
  c.plot_matplotlib()



greek_cross_with_pads
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.greek_cross_with_pads

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.greek_cross_with_pads(pad_spacing=150.0)
  c.plot_matplotlib()



hline
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.hline

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.hline(length=10.0, width=0.5, layer='WG', port_type='optical')
  c.plot_matplotlib()



interdigital_capacitor
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.interdigital_capacitor

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.interdigital_capacitor(fingers=4, finger_length=20.0, finger_gap=2.0, thickness=5.0, layer='WG')
  c.plot_matplotlib()



litho_calipers
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.litho_calipers

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.litho_calipers(notch_size=[2.0, 5.0], notch_spacing=2.0, num_notches=11, offset_per_notch=0.1, row_spacing=0.0, layer1='WG', layer2='SLAB150')
  c.plot_matplotlib()



litho_ruler
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.litho_ruler

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.litho_ruler(height=2, width=0.5, spacing=2.0, scale=[3, 1, 1, 1, 1, 2, 1, 1, 1, 1], num_marks=21, layer='WG')
  c.plot_matplotlib()



litho_steps
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.litho_steps

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.litho_steps(line_widths=[1.0, 2.0, 4.0, 8.0, 16.0], line_spacing=10.0, height=100.0, layer='WG')
  c.plot_matplotlib()



logo
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.logo

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.logo(text='GDSFACTORY')
  c.plot_matplotlib()



loop_mirror
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.loop_mirror

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.loop_mirror(bend90='bend_euler')
  c.plot_matplotlib()



loss_deembedding_ch12_34
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.loss_deembedding_ch12_34

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.loss_deembedding_ch12_34(pitch=127.0, input_port_indexes=[0, 2])
  c.plot_matplotlib()



loss_deembedding_ch13_24
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.loss_deembedding_ch13_24

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.loss_deembedding_ch13_24(pitch=127.0, input_port_indexes=[0, 1], cross_section='strip')
  c.plot_matplotlib()



loss_deembedding_ch14_23
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.loss_deembedding_ch14_23

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.loss_deembedding_ch14_23(pitch=127.0, input_port_indexes=[0, 1])
  c.plot_matplotlib()



marker_te
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.marker_te

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.marker_te(layer='TE', centered=True, port_type='placement', port_angles=[180, 90, 0, -90])
  c.plot_matplotlib()



marker_tm
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.marker_tm

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.marker_tm(layer='TM', centered=True, port_type='placement', port_angles=[180, 90, 0, -90])
  c.plot_matplotlib()



mmi1x2
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mmi1x2

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mmi1x2(width_taper=1.0, length_taper=10.0, length_mmi=5.5, width_mmi=2.5, gap_mmi=0.25, with_bbox=True, cross_section='strip')
  c.plot_matplotlib()



mmi1x2_with_sbend
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mmi1x2_with_sbend

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mmi1x2_with_sbend(with_sbend=True, cross_section='strip')
  c.plot_matplotlib()



mmi2x2
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mmi2x2

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mmi2x2(width_taper=1.0, length_taper=10.0, length_mmi=5.5, width_mmi=2.5, gap_mmi=0.25, with_bbox=True, cross_section='strip')
  c.plot_matplotlib()



mmi2x2_with_sbend
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mmi2x2_with_sbend

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mmi2x2_with_sbend(with_sbend=True, cross_section='strip')
  c.plot_matplotlib()



mmi_90degree_hybrid
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mmi_90degree_hybrid

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mmi_90degree_hybrid(width=0.5, width_taper=1.7, length_taper=40.0, length_mmi=175.0, width_mmi=10.0, gap_mmi=0.8, with_bbox=True, cross_section='strip')
  c.plot_matplotlib()



mode_converter
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mode_converter

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mode_converter(gap=0.3, length=10, mm_width=1.2, mc_mm_width=1, sm_width=0.5, taper_length=25, cross_section='strip')
  c.plot_matplotlib()



mzi
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi(delta_length=10.0, length_y=2.0, length_x=0.1, splitter='mmi1x2', with_splitter=True, port_e1_splitter='o2', port_e0_splitter='o3', port_e1_combiner='o2', port_e0_combiner='o3', nbends=2, cross_section='strip', mirror_bot=False, add_optical_ports_arms=False)
  c.plot_matplotlib()



mzi1x2_2x2
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi1x2_2x2

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi1x2_2x2(delta_length=10.0, length_y=2.0, length_x=0.1, splitter='mmi1x2', with_splitter=True, port_e1_splitter='o2', port_e0_splitter='o3', port_e1_combiner='o3', port_e0_combiner='o4', nbends=2, cross_section='strip', mirror_bot=False, add_optical_ports_arms=False)
  c.plot_matplotlib()



mzi2x2_2x2
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi2x2_2x2

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi2x2_2x2(delta_length=10.0, length_y=2.0, length_x=0.1, with_splitter=True, port_e1_splitter='o3', port_e0_splitter='o4', port_e1_combiner='o3', port_e0_combiner='o4', nbends=2, cross_section='strip', mirror_bot=False, add_optical_ports_arms=False)
  c.plot_matplotlib()



mzi_arm
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi_arm

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi_arm(length_y_left=0.8, length_y_right=0.8, length_x=0.1)
  c.plot_matplotlib()



mzi_arms
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi_arms

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi_arms(delta_length=10.0, length_y=0.8, length_x=0.1, with_splitter=True, delta_yright=0)
  c.plot_matplotlib()



mzi_coupler
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi_coupler

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi_coupler(delta_length=10.0, length_y=2.0, length_x=0.1, with_splitter=True, port_e1_splitter='o3', port_e0_splitter='o4', port_e1_combiner='o3', port_e0_combiner='o4', nbends=2, cross_section='strip', mirror_bot=False, add_optical_ports_arms=False)
  c.plot_matplotlib()



mzi_lattice
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi_lattice

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi_lattice(coupler_lengths=[10.0, 20.0], coupler_gaps=[0.2, 0.3], delta_lengths=[10.0])
  c.plot_matplotlib()



mzi_lattice_mmi
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi_lattice_mmi

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi_lattice_mmi(coupler_widths=[None, None], coupler_widths_tapers=[1.0, 1.0], coupler_lengths_tapers=[10.0, 10.0], coupler_lengths_mmis=[5.5, 5.5], coupler_widths_mmis=[2.5, 2.5], coupler_gaps_mmis=[0.25, 0.25], taper_functions_mmis=[{'function': 'taper'}, {'function': 'taper'}], straight_functions_mmis=[{'function': 'straight'}, {'function': 'straight'}], cross_sections_mmis=['strip', 'strip'], delta_lengths=[10.0])
  c.plot_matplotlib()



mzi_pads_center
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi_pads_center

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi_pads_center(length_x=500, length_y=40, mzi_sig_top='top_e2', mzi_gnd_top='top_e1', mzi_sig_bot='bot_e1', mzi_gnd_bot='bot_e2', pad_sig_bot='e1_1_1', pad_sig_top='e3_1_3', pad_gnd_bot='e4_1_2', pad_gnd_top='e2_1_2', delta_length=40.0, cross_section='strip', cross_section_metal='metal_routing', pad_spacing='pad_spacing')
  c.plot_matplotlib()



mzi_phase_shifter
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi_phase_shifter

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi_phase_shifter(delta_length=10.0, length_y=2.0, length_x=200, straight_x_top='straight_heater_metal', splitter='mmi1x2', with_splitter=True, port_e1_splitter='o2', port_e0_splitter='o3', port_e1_combiner='o2', port_e0_combiner='o3', nbends=2, cross_section='strip', mirror_bot=False, add_optical_ports_arms=False)
  c.plot_matplotlib()



mzi_phase_shifter_top_heater_metal
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzi_phase_shifter_top_heater_metal

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzi_phase_shifter_top_heater_metal(delta_length=10.0, length_y=2.0, length_x=200, splitter='mmi1x2', with_splitter=True, port_e1_splitter='o2', port_e0_splitter='o3', port_e1_combiner='o2', port_e0_combiner='o3', nbends=2, cross_section='strip', mirror_bot=False, add_optical_ports_arms=False)
  c.plot_matplotlib()



mzit
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzit

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzit(w0=0.5, w1=0.45, w2=0.55, dy=2.0, delta_length=10.0, length=1.0, coupler_length1=5.0, coupler_length2=10.0, coupler_gap1=0.2, coupler_gap2=0.3, taper_length=5.0)
  c.plot_matplotlib()



mzit_lattice
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzit_lattice

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzit_lattice(coupler_lengths=[10.0, 20.0], coupler_gaps=[0.2, 0.3], delta_lengths=[10.0])
  c.plot_matplotlib()



mzm
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.mzm

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.mzm(length_x=500, length_y=2.0, delta_length=0.0, splitter='mmi1x2', combiner='mmi1x2', with_splitter=True, port_e1_splitter='o2', port_e0_splitter='o3', port_e1_combiner='o2', port_e0_combiner='o3', nbends=2, cross_section='strip', mirror_bot=False)
  c.plot_matplotlib()



nxn
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.nxn

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.nxn(west=1, east=4, north=0, south=0, xsize=8.0, ysize=8.0, wg_width=0.5, layer='WG', wg_margin=1.0)
  c.plot_matplotlib()



optimal_90deg
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.optimal_90deg

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.optimal_90deg(width=100, num_pts=15, length_adjust=1, layer=[1, 0])
  c.plot_matplotlib()



optimal_hairpin
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.optimal_hairpin

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.optimal_hairpin(width=0.2, pitch=0.6, length=10, turn_ratio=4, num_pts=50, layer=[1, 0])
  c.plot_matplotlib()



optimal_step
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.optimal_step

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.optimal_step(start_width=10, end_width=22, num_pts=50, width_tol=0.001, anticrowding_factor=1.2, symmetric=False, layer=[1, 0])
  c.plot_matplotlib()



pack_doe
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pack_doe

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pack_doe(doe='mmi1x2', do_permutations=False)
  c.plot_matplotlib()



pack_doe_grid
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pack_doe_grid

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pack_doe_grid(doe='mmi1x2', do_permutations=False, with_text=False)
  c.plot_matplotlib()



pad
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pad

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pad(size=[100.0, 100.0], layer='MTOP', port_inclusion=0)
  c.plot_matplotlib()



pad_array
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pad_array

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pad_array(pad='pad', spacing=[150.0, 150.0], columns=6, rows=1, angle=270)
  c.plot_matplotlib()



pad_array0
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pad_array0

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pad_array0(pad='pad', spacing=[150.0, 150.0], columns=1, rows=3, angle=0)
  c.plot_matplotlib()



pad_array180
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pad_array180

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pad_array180(pad='pad', spacing=[150.0, 150.0], columns=1, rows=3, angle=180)
  c.plot_matplotlib()



pad_array270
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pad_array270

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pad_array270(pad='pad', spacing=[150.0, 150.0], columns=6, rows=1, angle=270)
  c.plot_matplotlib()



pad_array90
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pad_array90

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pad_array90(pad='pad', spacing=[150.0, 150.0], columns=6, rows=1, angle=90)
  c.plot_matplotlib()



pad_gsg_open
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pad_gsg_open

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pad_gsg_open(size=[22, 7], layer_metal='M3', metal_spacing=5.0, short=False, pad_spacing=150)
  c.plot_matplotlib()



pad_gsg_short
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pad_gsg_short

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pad_gsg_short(size=[22, 7], layer_metal='M3', metal_spacing=5.0, short=True, pad_spacing=150)
  c.plot_matplotlib()



pad_rectangular
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pad_rectangular

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pad_rectangular(size='pad_size', layer='MTOP', port_inclusion=0)
  c.plot_matplotlib()



pads_shorted
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pads_shorted

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pads_shorted(columns=8, pad_spacing=150.0, layer_metal='M3', metal_width=10)
  c.plot_matplotlib()



pixel
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.pixel

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.pixel(size=1.0, layer='WG')
  c.plot_matplotlib()



polarization_splitter_rotator
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.polarization_splitter_rotator

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.polarization_splitter_rotator(width_taper_in=[0.54, 0.69, 0.83], length_taper_in=[4.0, 44.0], width_coupler=[0.9, 0.405], length_coupler=7.0, gap=0.15, width_out=0.54, length_out=14.33, dy=5.0, cross_section='strip')
  c.plot_matplotlib()



qrcode
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.qrcode

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.qrcode(data='mask01', psize=1, layer='WG')
  c.plot_matplotlib()



ramp
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ramp

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ramp(length=10.0, width1=5.0, width2=8.0, layer='WG')
  c.plot_matplotlib()



rectangle
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.rectangle

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.rectangle(size=[4.0, 2.0], layer='WG', centered=False, port_type='placement', port_angles=[180, 90, 0, -90])
  c.plot_matplotlib()



rectangle_with_slits
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.rectangle_with_slits

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.rectangle_with_slits(size=[100.0, 200.0], layer='WG', layer_slit='SLAB150', centered=False, slit_size=[1.0, 1.0], slit_spacing=[20, 20], slit_enclosure=10)
  c.plot_matplotlib()



regular_polygon
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.regular_polygon

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.regular_polygon(sides=6, side_length=10, layer='WG', port_type='placement')
  c.plot_matplotlib()



resistance_meander
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.resistance_meander

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.resistance_meander(pad_size=[50.0, 50.0], num_squares=1000, width=1.0, res_layer='MTOP', pad_layer='MTOP', gnd_layer='MTOP')
  c.plot_matplotlib()



resistance_sheet
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.resistance_sheet

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.resistance_sheet(width=10, layers=['SLAB90', 'NPP'], layer_offsets=[0, 0.2], pad_pitch=100.0, port_angle1=180, port_angle2=0)
  c.plot_matplotlib()



ring
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring(radius=10.0, width=0.5, angle_resolution=2.5, layer='WG', angle=360)
  c.plot_matplotlib()



ring_crow
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_crow

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_crow()
  c.plot_matplotlib()



ring_crow_couplers
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_crow_couplers

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_crow_couplers()
  c.plot_matplotlib()



ring_double
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_double

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_double(gap=0.2, radius=10.0, length_x=0.01, length_y=0.01, cross_section='strip')
  c.plot_matplotlib()



ring_double_heater
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_double_heater

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_double_heater(gap=0.2, radius=10.0, length_x=0.01, length_y=0.01, cross_section_heater='heater_metal', cross_section_waveguide_heater='strip_heater_metal', cross_section='strip', port_angle=90, via_stack_offset=[0, 0])
  c.plot_matplotlib()



ring_double_pn
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_double_pn

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_double_pn(add_gap=0.3, drop_gap=0.3, radius=5.0, doping_angle=85, doped_heater=True, doped_heater_angle_buffer=10, doped_heater_layer='NPP', doped_heater_width=0.5, doped_heater_waveguide_offset=2.175)
  c.plot_matplotlib()



ring_double_trenches
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_double_trenches

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_double_trenches(cross_section='rib_with_trenches', top=True, bot=True, right=False, left=False)
  c.plot_matplotlib()



ring_section_based
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_section_based

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_section_based(gap=0.3, radius=5.0, add_drop=False, cross_sections_sequence='AB', start_angle=10.0, bus_cross_section='strip', ang_res=0.1)
  c.plot_matplotlib()



ring_single
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_single

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_single(gap=0.2, radius=10.0, length_x=4.0, length_y=0.6, cross_section='strip')
  c.plot_matplotlib()



ring_single_array
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_single_array

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_single_array(spacing=5.0, cross_section='strip')
  c.plot_matplotlib()



ring_single_bend_coupler
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_single_bend_coupler

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_single_bend_coupler(radius=5.0, gap=0.2, coupling_angle_coverage=180.0, length_y=0.6, cross_section_inner='strip', cross_section_outer='strip')
  c.plot_matplotlib()



ring_single_dut
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_single_dut

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_single_dut(gap=0.2, length_x=4, length_y=0, radius=5.0, with_component=True, port_name='o1')
  c.plot_matplotlib()



ring_single_heater
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_single_heater

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_single_heater(gap=0.2, radius=10.0, length_x=4.0, length_y=0.6, cross_section_waveguide_heater='strip_heater_metal', cross_section='strip', port_angle=90, via_stack_offset=[0, 0])
  c.plot_matplotlib()



ring_single_pn
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_single_pn

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_single_pn(gap=0.3, radius=5.0, doping_angle=250, doped_heater=True, doped_heater_angle_buffer=10, doped_heater_layer='NPP', doped_heater_width=0.5, doped_heater_waveguide_offset=2.175)
  c.plot_matplotlib()



ring_single_trenches
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.ring_single_trenches

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.ring_single_trenches(cross_section='rib_with_trenches', top=True, bot=True, right=False, left=False)
  c.plot_matplotlib()



seal_ring
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.seal_ring

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.seal_ring(bbox=[[-1.0, -1.0], [3.0, 4.0]], width=10, padding=10.0, with_north=True, with_south=True, with_east=True, with_west=True)
  c.plot_matplotlib()



snspd
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.snspd

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.snspd(wire_width=0.2, wire_pitch=0.6, size=[10, 8], turn_ratio=4, terminals_same_side=False, layer=[1, 0])
  c.plot_matplotlib()



spiral_double
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.spiral_double

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.spiral_double(min_bend_radius=10.0, separation=2.0, number_of_loops=3, npoints=1000, cross_section='strip')
  c.plot_matplotlib()



spiral_external_io
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.spiral_external_io

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.spiral_external_io(N=6, x_inner_length_cutback=300.0, x_inner_offset=0.0, y_straight_inner_top=0.0, xspacing=3.0, yspacing=3.0, cross_section='strip', with_inner_ports=False, y_straight_outer_offset=0.0, inner_loop_spacing_offset=0.0)
  c.plot_matplotlib()



spiral_inner_io
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.spiral_inner_io

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.spiral_inner_io(N=6, x_straight_inner_right=150.0, x_straight_inner_left=50.0, y_straight_inner_top=50.0, y_straight_inner_bottom=10.0, grating_spacing=127.0, waveguide_spacing=3.0, cross_section='strip', asymmetric_cross_section=False)
  c.plot_matplotlib()



spiral_inner_io_fiber_single
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.spiral_inner_io_fiber_single

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.spiral_inner_io_fiber_single(cross_section='strip', x_straight_inner_right=40.0, x_straight_inner_left=75.0, y_straight_inner_top=10.0, y_straight_inner_bottom=0.0, grating_spacing=200.0)
  c.plot_matplotlib()



spiral_racetrack
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.spiral_racetrack

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.spiral_racetrack(min_radius=5, straight_length=10.0, spacings=[2, 2, 3, 3, 2, 2], cross_section='strip', with_inner_ports=False, extra_90_deg_bend=False)
  c.plot_matplotlib()



spiral_racetrack_fixed_length
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.spiral_racetrack_fixed_length

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.spiral_racetrack_fixed_length(length=1000, in_out_port_spacing=150, n_straight_sections=8, min_radius=5, min_spacing=5.0, cross_section='strip', with_inner_ports=False)
  c.plot_matplotlib()



spiral_racetrack_heater_doped
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.spiral_racetrack_heater_doped

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.spiral_racetrack_heater_doped(straight_length=30, spacing=2, num=8, waveguide_cross_section='strip', heater_cross_section='npp')
  c.plot_matplotlib()



spiral_racetrack_heater_metal
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.spiral_racetrack_heater_metal

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.spiral_racetrack_heater_metal(straight_length=30, spacing=2, num=8, waveguide_cross_section='strip', heater_cross_section='heater_metal')
  c.plot_matplotlib()



splitter_chain
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.splitter_chain

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.splitter_chain(columns=3)
  c.plot_matplotlib()



splitter_tree
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.splitter_tree

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.splitter_tree(noutputs=4, spacing=[90.0, 50.0], cross_section='strip')
  c.plot_matplotlib()



staircase
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.staircase

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.staircase(length_v=5.0, length_h=5.0, rows=4)
  c.plot_matplotlib()



straight
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight(length=10.0, npoints=2, with_bbox=True, cross_section='strip')
  c.plot_matplotlib()



straight_array
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_array

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_array(n=4, spacing=4.0)
  c.plot_matplotlib()



straight_heater_doped_rib
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_heater_doped_rib

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_heater_doped_rib(length=320.0, nsections=3, via_stack_metal_size=[10.0, 10.0], via_stack_size=[10.0, 10.0], with_taper1=True, with_taper2=True, heater_width=2.0, heater_gap=0.8, via_stack_gap=0.0, width=0.5, xoffset_tip1=0.2, xoffset_tip2=0.4)
  c.plot_matplotlib()



straight_heater_doped_strip
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_heater_doped_strip

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_heater_doped_strip(length=320.0, nsections=3, via_stack_metal_size=[10.0, 10.0], via_stack_size=[10.0, 10.0], with_taper1=True, with_taper2=True, heater_width=2.0, heater_gap=0.8, via_stack_gap=0.0, width=0.5, xoffset_tip1=0.2, xoffset_tip2=0.4)
  c.plot_matplotlib()



straight_heater_meander
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_heater_meander

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_heater_meander(length=300.0, spacing=2.0, cross_section='strip', heater_width=2.5, extension_length=15.0, layer_heater='HEATER', radius=5.0, via_stack='via_stack_heater_mtop', port_angle1=180, port_angle2=0, heater_taper_length=10.0, straight_widths=[0.8, 0.9, 0.8], taper_length=10)
  c.plot_matplotlib()



straight_heater_meander_doped
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_heater_meander_doped

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_heater_meander_doped(length=300.0, spacing=2.0, cross_section='strip', heater_width=1.5, extension_length=15.0, layers_doping=['P', 'PP', 'PPP'], radius=5.0, port_angle1=180, port_angle2=0, straight_widths=[0.8, 0.9, 0.8], taper_length=10)
  c.plot_matplotlib()



straight_heater_metal
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_heater_metal

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_heater_metal(length=320.0, length_undercut_spacing=6.0, length_undercut=30.0, length_straight_input=15.0, heater_width=2.5, cross_section_heater='heater_metal', cross_section_waveguide_heater='strip_heater_metal', cross_section_heater_undercut='strip_heater_metal_undercut', with_undercut=False, via_stack='via_stack_heater_mtop', port_angle1=180, port_angle2=0, heater_taper_length=5.0)
  c.plot_matplotlib()



straight_heater_metal_90_90
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_heater_metal_90_90

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_heater_metal_90_90(length=320.0, length_undercut_spacing=6.0, length_undercut=30.0, length_straight_input=15.0, heater_width=2.5, cross_section_heater='heater_metal', cross_section_waveguide_heater='strip_heater_metal', cross_section_heater_undercut='strip_heater_metal_undercut', with_undercut=False, via_stack='via_stack_heater_mtop', port_angle1=90, port_angle2=90, heater_taper_length=5.0)
  c.plot_matplotlib()



straight_heater_metal_undercut
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_heater_metal_undercut

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_heater_metal_undercut(length=320.0, length_undercut_spacing=6.0, length_undercut=30.0, length_straight_input=15.0, heater_width=2.5, cross_section_heater='heater_metal', cross_section_waveguide_heater='strip_heater_metal', cross_section_heater_undercut='strip_heater_metal_undercut', with_undercut=True, via_stack='via_stack_heater_mtop', port_angle1=180, port_angle2=0, heater_taper_length=5.0)
  c.plot_matplotlib()



straight_heater_metal_undercut_90_90
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_heater_metal_undercut_90_90

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_heater_metal_undercut_90_90(length=320.0, length_undercut_spacing=6.0, length_undercut=30.0, length_straight_input=15.0, heater_width=2.5, cross_section_heater='heater_metal', cross_section_waveguide_heater='strip_heater_metal', cross_section_heater_undercut='strip_heater_metal_undercut', with_undercut=False, via_stack='via_stack_heater_mtop', port_angle1=90, port_angle2=90, heater_taper_length=5.0)
  c.plot_matplotlib()



straight_pin
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_pin

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_pin(length=500.0, via_stack_width=10.0, via_stack_spacing=2)
  c.plot_matplotlib()



straight_pin_slot
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_pin_slot

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_pin_slot(length=500.0, via_stack_width=10.0, via_stack_spacing=3.0, via_stack_slab_spacing=2.0)
  c.plot_matplotlib()



straight_pn
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_pn

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_pn(length=2000, via_stack_width=10.0, via_stack_spacing=2)
  c.plot_matplotlib()



straight_rib
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_rib

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_rib(length=10.0, npoints=2, with_bbox=True)
  c.plot_matplotlib()



straight_rib_tapered
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.straight_rib_tapered

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.straight_rib_tapered(length=5.0, port1='o2', port2='o1', port_type='optical', centered=False)
  c.plot_matplotlib()



switch_tree
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.switch_tree

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.switch_tree(noutputs=4, spacing=[500, 100], cross_section='strip')
  c.plot_matplotlib()



taper
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper(length=10.0, width1=0.5, with_bbox=True, with_two_ports=True, cross_section='strip')
  c.plot_matplotlib()



taper2
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper2

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper2(length=10.0, width1=0.5, width2=3, with_bbox=True, with_two_ports=True, cross_section='strip')
  c.plot_matplotlib()



taper_0p5_to_3_l36
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_0p5_to_3_l36

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_0p5_to_3_l36(cross_section='strip')
  c.plot_matplotlib()



taper_adiabatic
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_adiabatic

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_adiabatic(width1=0.5, width2=5.0, length=0, alpha=1, wavelength=1.55, npoints=200, cross_section='strip')
  c.plot_matplotlib()



taper_cross_section_linear
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_cross_section_linear

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_cross_section_linear(length=10, npoints=2, linear=True, width_type='sine')
  c.plot_matplotlib()



taper_cross_section_parabolic
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_cross_section_parabolic

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_cross_section_parabolic(length=10, npoints=101, linear=False, width_type='parabolic')
  c.plot_matplotlib()



taper_cross_section_sine
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_cross_section_sine

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_cross_section_sine(length=10, npoints=101, linear=False, width_type='sine')
  c.plot_matplotlib()



taper_from_csv
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_from_csv

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_from_csv(cross_section='strip')
  c.plot_matplotlib()



taper_parabolic
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_parabolic

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_parabolic(length=20, width1=0.5, width2=5.0, exp=0.5, npoints=100, layer='WG')
  c.plot_matplotlib()



taper_sc_nc
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_sc_nc

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_sc_nc(length=20.0, width1=0.5, width2=0.15, w_slab1=0.15, w_slab2=1.0, layer_wg='WG', layer_slab='WGN', cross_section='strip')
  c.plot_matplotlib()



taper_strip_to_ridge
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_strip_to_ridge

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_strip_to_ridge(length=10.0, width1=0.5, width2=0.5, w_slab1=0.15, w_slab2=6.0, layer_wg='WG', layer_slab='SLAB90', cross_section='strip')
  c.plot_matplotlib()



taper_strip_to_ridge_trenches
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_strip_to_ridge_trenches

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_strip_to_ridge_trenches(length=10.0, width=0.5, slab_offset=3.0, trench_width=2.0, trench_layer='DEEP_ETCH', layer_wg='WG', trench_offset=0.1)
  c.plot_matplotlib()



taper_w10_l100
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_w10_l100

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_w10_l100(cross_section='strip')
  c.plot_matplotlib()



taper_w10_l150
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_w10_l150

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_w10_l150(cross_section='strip')
  c.plot_matplotlib()



taper_w10_l200
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_w10_l200

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_w10_l200(cross_section='strip')
  c.plot_matplotlib()



taper_w11_l200
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_w11_l200

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_w11_l200(cross_section='strip')
  c.plot_matplotlib()



taper_w12_l200
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.taper_w12_l200

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.taper_w12_l200(cross_section='strip')
  c.plot_matplotlib()



terminator
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.terminator

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.terminator(length=50, cross_section_input='strip', tapered_width=0.2, doping_layers=['NPP'])
  c.plot_matplotlib()



text
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.text

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.text(text='abcd', size=10.0, position=[0, 0], justify='left', layer='WG')
  c.plot_matplotlib()



text_freetype
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.text_freetype

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.text_freetype(text='abcd', size=10, justify='left', layer='WG', font='DEPLOF')
  c.plot_matplotlib()



text_lines
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.text_lines

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.text_lines(text=['Chip', '01'], size=0.4, layer='WG')
  c.plot_matplotlib()



text_rectangular
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.text_rectangular

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.text_rectangular(text='abcd', size=10.0, position=[0.0, 0.0], justify='left', layer='WG')
  c.plot_matplotlib()



text_rectangular_multi_layer
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.text_rectangular_multi_layer

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.text_rectangular_multi_layer(text='abcd', layers=['WG', 'M1', 'M2', 'M3'])
  c.plot_matplotlib()



triangle
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.triangle

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.triangle(x=10, xtop=0, y=20, ybot=0, layer='WG')
  c.plot_matplotlib()



verniers
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.verniers

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.verniers(widths=[0.1, 0.2, 0.3, 0.4, 0.5], gap=0.1, xsize=100, layer_label='LABEL')
  c.plot_matplotlib()



version_stamp
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.version_stamp

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.version_stamp(labels=['demo_label'], with_qr_code=False, layer='WG', pixel_size=1, text_size=10)
  c.plot_matplotlib()



via
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via(size=[0.7, 0.7], spacing=[2.0, 2.0], enclosure=1.0, layer='VIAC', bbox_offset=0)
  c.plot_matplotlib()



via1
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via1

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via1(size=[0.7, 0.7], spacing=[2.0, 2.0], enclosure=2, layer='VIA1', bbox_offset=0)
  c.plot_matplotlib()



via2
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via2

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via2(size=[0.7, 0.7], spacing=[2.0, 2.0], enclosure=1.0, layer='VIA2', bbox_offset=0)
  c.plot_matplotlib()



via_corner
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via_corner

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via_corner(cross_section=[[{'function': 'cross_section', 'settings': {'layer': 'M2', 'width': 10.0, 'port_names': ['e1', 'e2'], 'port_types': ['electrical', 'electrical'], 'radius': None, 'min_length': 5, 'gap': 5}}, [0, 180]], [{'function': 'cross_section', 'settings': {'layer': 'M3', 'width': 10.0, 'port_names': ['e1', 'e2'], 'port_types': ['electrical', 'electrical'], 'radius': None, 'min_length': 5, 'gap': 5}}, [90, 270]]], layers_labels=['m2', 'm3'])
  c.plot_matplotlib()



via_cutback
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via_cutback

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via_cutback(num_vias=100.0, wire_width=10.0, via_width=5.0, via_spacing=40.0, min_pad_spacing=0.0, pad_size=[150, 150], layer1='HEATER', layer2='M1', via_layer='VIAC', wire_pad_inclusion=12.0)
  c.plot_matplotlib()



via_stack
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via_stack

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via_stack(size=[11.0, 11.0], layers=['M1', 'M2', 'M3'], correct_size=True)
  c.plot_matplotlib()



via_stack_from_rules
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via_stack_from_rules

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via_stack_from_rules(size=[1.2, 1.2], layers=['M1', 'M2', 'M3'], via_min_size=[[0.2, 0.2], [0.2, 0.2]], via_min_gap=[[0.1, 0.1], [0.1, 0.1]], via_min_enclosure=[0.15, 0.25])
  c.plot_matplotlib()



via_stack_heater_m3
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via_stack_heater_m3

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via_stack_heater_m3(size=[11.0, 11.0], layers=['HEATER', 'M2', 'M3'], correct_size=True)
  c.plot_matplotlib()



via_stack_heater_mtop
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via_stack_heater_mtop

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via_stack_heater_mtop(size=[11.0, 11.0], layers=['HEATER', 'M2', 'M3'], correct_size=True)
  c.plot_matplotlib()



via_stack_slab_m3
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via_stack_slab_m3

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via_stack_slab_m3(size=[11.0, 11.0], layers=['SLAB90', 'M1', 'M2', 'M3'], correct_size=True)
  c.plot_matplotlib()



via_stack_slot
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via_stack_slot

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via_stack_slot(size=[11.0, 11.0], layers=['M1', 'M2'], layer_offsets=[0, 1.0], enclosure=1.0, ysize=0.5, yspacing=2.0)
  c.plot_matplotlib()



via_stack_slot_m1_m2
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via_stack_slot_m1_m2

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via_stack_slot_m1_m2(size=[11.0, 11.0], layers=['M1', 'M2'], layer_offsets=[0, 1.0], enclosure=1.0, ysize=0.5, yspacing=2.0)
  c.plot_matplotlib()



via_stack_with_offset
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.via_stack_with_offset

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.via_stack_with_offset(layers=['PPP', 'M1'], size=[10, 10])
  c.plot_matplotlib()



viac
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.viac

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.viac(size=[0.7, 0.7], spacing=[2.0, 2.0], enclosure=1.0, layer='VIAC', bbox_offset=0)
  c.plot_matplotlib()



wafer
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.wafer

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.wafer(reticle='die', cols=[2, 6, 6, 8, 8, 6, 6, 2])
  c.plot_matplotlib()



wire_corner
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.wire_corner

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.wire_corner(cross_section='metal_routing')
  c.plot_matplotlib()



wire_corner45
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.wire_corner45

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.wire_corner45(cross_section='metal_routing', radius=10)
  c.plot_matplotlib()



wire_sbend
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.wire_sbend

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.wire_sbend(dx=20.0, dy=10.0)
  c.plot_matplotlib()



wire_straight
----------------------------------------------------

.. autofunction:: gdsfactory.pcells.wire_straight

.. plot::
  :include-source:

  import gdsfactory as gf

  c = gf.pcells.wire_straight(length=10.0, npoints=2, with_bbox=True, cross_section='metal_routing')
  c.plot_matplotlib()
