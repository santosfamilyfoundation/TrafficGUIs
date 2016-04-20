#! /usr/bin/env python
import storage
import sqlite3


def main(filename):
    """
    Creates a new table in the specified database called "object_trajectories". This table
    has row labels "object_id", "frame", "x", "y", "x_v", "y_v".

        Args:
            filename (str): Filename/path to a .sqlite database file. This should be generated
                by TrafficIntelligence and store tracked features and objects.

        Returns:
            None
    """
    connection = sqlite3.connect(filename)
    positions = storage.loadTrajectoriesFromTable(connection, "positions", "object")
    velocities = storage.loadTrajectoriesFromTable(connection, "velocities", "object")

    if len(velocities) > 0:
        for o, v in zip(positions, velocities):
            if o.num == v.num:
                o.velocities = v.positions
                # avoid having velocity shorter by one position than positions
                o.velocities.duplicateLastPosition()
            else:
                print('Could not match positions {0} with velocities {1}'.format(
                    o.num, v.num))
    cur = connection.cursor()
    create_table(cur)
    for obj in positions:
        print obj.num
        frames = range(obj.timeInterval.first, obj.timeInterval.last + 1)
        for f, frame in enumerate(frames):
            x, y = obj.positions[f]
            xv, yv = obj.velocities[f]
            write_row(cur, obj.num, frame, x, y, xv, yv)
    connection.commit()
    connection.close()


def write_row(cur, object_id, frame, x_pos, y_pos, x_vel, y_vel):
    """
    Writes a row to the object_trajectories table.

        Args:
            cur (sqlite3 Cursor): Cursor to the database to update.
            object_id (int): Numerical object identifier
            frame (int): Video frame number which corresponds to the given trajectory and velocity coordinates.
            x_pos (num): x-position of the specified object in the specified video frame. Coordinate is in world
                coordinates--the homography is required to transform into image-coordinates.
            y_pos (num): y-position of the specified object in the specified video frame. Coordinate is in world
                coordinates--the homography is required to transform into image-coordinates.
            x_vel (num): x-component of the specified object's velocity in the specified video frame. Units are in homography
                units per frame.
            y_vel (num): y-component of the specified object's velocity in the specified video frame. Units are in homography
                units per frame.

        Returns:
            None
    """
    cur.execute("INSERT INTO object_trajectories VALUES ({o}, {f}, {xp}, {yp}, {xv}, {yv})".format(
        o=object_id,
        f=frame,
        xp=x_pos,
        yp=y_pos,
        xv=x_vel,
        yv=y_vel))


def create_table(cur):
    """
    Creates the `object_trajectories` table if it does not already exist.

        Args:
            cur (sqlite Cursor): Cursor object of the sqlite database in which the `object_trajectories` table should be created.

        Returns:
            None
    """
    cur.execute('CREATE TABLE IF NOT EXISTS object_trajectories (object_id INTEGER, frame INTEGER, x INTEGER, y INTEGER, x_v INTEGER, y_v INTEGER)')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Add \'object_trajectories\' table to a specified database of tracked features and objects.')
    parser.add_argument('db', metavar='<.sqlite database file>', help='A TrafficIntelligence generated .sqlite database.')

    args = parser.parse_args()
    main(args.db)