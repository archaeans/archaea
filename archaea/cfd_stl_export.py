import sys
import getopt
from archaea.simulation_objects.domain import Domain
from archaea.geometry.point3d import Point3d


def cfd_stl_export(argv):
    # Default values
    arg_domain_width = 100.0
    arg_domain_depth = 50.0
    arg_domain_height = 50.0
    arg_number_of_storeys = 1
    arg_number_of_rooms = 3
    arg_courtyard_width = 10.0
    arg_room_width = 4.0
    arg_room_depth = 4.0
    arg_room_height = 3.0
    arg_room_wall_thickness = 0.1
    arg_room_window_existence = 1
    arg_room_window_width = 0.6
    arg_room_window_height = 1.2
    arg_room_door_existence = 1
    arg_room_door_width = 0.8
    arg_room_door_height = 2.0

    arg_help = "{0}\n\n" \
               "Welcome to stl exporter program for cfd calculations! \n" \
               "Use below flags to generate stl.\n" \
               " -dw\t--domain-width               <domain_width>            default: 100.0\n" \
               " -dd\t--domain-depth               <domain_depth>            default: 50.0\n" \
               " -dh\t--domain-height              <domain_height>           default: 50.0\n" \
               " -nos\t--number-of-storeys         <number_of_storeys>        default: 1\n" \
               " -nor\t--number-of-rooms           <number_of_rooms>          default: 3\n" \
               " -cw\t--courtyard-width            <courtyard_width>         default: 10.0\n" \
               " -rw\t--room-width                 <room_width>              default: 4.0\n" \
               " -rd\t--room-depth                 <room_depth>              default: 4.0\n" \
               " -rh\t--room-height                <room_height>             default: 3.0\n" \
               " -rwt\t--room-wall-thickness       <room_wall_thickness>      default: 0.1\n" \
               " -rwe\t--room-window-existence     <room_window_existence>    default: 1\n" \
               " -rww\t--room-window-width         <room_window_width>        default: 0.6\n" \
               " -rwh\t--room-window-height        <room_window_height>       default: 1.2\n" \
               " -rde\t--room-door-existence       <room_door_existence>      default: 1\n" \
               " -rdw\t--room-door-width           <room_door_width>          default: 0.8\n" \
               " -rdh\t--room-door-height          <room_door_height>         default: 2.0\n".format(argv[0])

    try:
        opts, args = getopt.getopt(argv[1:], "hdw:dd:dh:nos:nor:cw:rw:rd:rh:rwt:rwe:rww:rwh:rde:rdw:rdh:",
                                   ["help",
                                    "domain-width=",
                                    "domain-depth=",
                                    "domain-height=",
                                    "number-of-storeys=",
                                    "number-of-rooms=",
                                    "courtyard-width=",
                                    "room-width=",
                                    "room-depth=",
                                    "room-height=",
                                    "room-wall-thickness=",
                                    "room-window-existence=",
                                    "room-wall-width=",
                                    "room-wall-height=",
                                    "room-door-existence=",
                                    "room-door-width=",
                                    "room-door-height="])
    except ValueError:
        print(arg_help)
        sys.exit(2)

    # if user does not provide any argument, print help message
    if len(opts) == 0:
        print(arg_help)  # print the help message
        print("NOTE: Stl generated with default parameters because no argument provided.\n")

    # Find the upcoming flag and set it to it's value
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(arg_help)  # print the help message
            sys.exit(2)
        elif opt in ("-dw", "--domain-width"):
            arg_domain_width = arg
        elif opt in ("-dd", "--domain_depth"):
            arg_domain_depth = arg
        elif opt in ("-dh", "--domain_height"):
            arg_domain_height = arg
        elif opt in ("-nos", "--number-of-storeys"):
            arg_number_of_storeys = arg
        elif opt in ("-nor", "--number-of-rooms"):
            arg_number_of_rooms = arg
        elif opt in ("-cw", "--courtyard-width"):
            arg_courtyard_width = arg
        elif opt in ("-rw", "--room-width"):
            arg_room_width = arg
        elif opt in ("-rd", "--room-depth"):
            arg_room_depth = arg
        elif opt in ("-rh", "--room-height"):
            arg_room_height = arg
        elif opt in ("-rwt", "--room-wall-thickness"):
            arg_room_wall_thickness = arg
        elif opt in ("-rwe", "--room-window-existence"):
            arg_room_window_existence = arg
        elif opt in ("-rww", "--room-window-width"):
            arg_room_window_width = arg
        elif opt in ("-rwh", "--room-window-height"):
            arg_room_window_height = arg
        elif opt in ("-dwe", "--door-window-existence"):
            arg_room_door_existence = arg
        elif opt in ("-dww", "--door-window-width"):
            arg_room_door_width = arg
        elif opt in ("-dwh", "--door-window-height"):
            arg_room_door_height = arg

    domain = Domain(Point3d.origin(), arg_domain_width, arg_domain_depth, arg_domain_height)


if __name__ == "__main__":
    cfd_stl_export(sys.argv)
