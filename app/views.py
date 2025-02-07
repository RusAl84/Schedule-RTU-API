from schedule_parser.models import WorkingData, db
from schedule_parser.main import parse_schedule
from app import app
from flask import Flask, flash, request, redirect, url_for, session, jsonify, render_template, make_response, Response
import requests
from os import environ
# from connect import connect_to_sqlite
import datetime as dt
from datetime import datetime, date, time

from app.schedule import get_full_schedule_by_weeks, get_groups_info, get_rooms_info, get_schedule_by_week, today_sch, tomorrow_sch, week_sch, next_week_sch, get_groups_old, full_sched, cur_week, get_lessons_list

import sys
from schedule_parser.get_or_create import get_or_create

sys.path.append('..')


@app.route('/api/schedule/<string:group>/today', methods=["GET"])
def today(group):
    """Today's schedule for requested group
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true

    definitions:

      teacher:
        type: object
        properties:
          id: 
            type: integer
          name: 
            type: string

      call:
        type: object
        properties:
          id: 
            type: integer
          call_num: 
            type: integer
          begin_time: 
            type: string
          end_time: 
            type: string

      discipline:
        type: object
        properties:
          id: 
            type: integer
          name: 
            type: string
      
      place:
        type: object
        properties:
          id: 
            type: integer
          short_name: 
            type: string
          name: 
            type: string

      room:
        type: object
        properties:
          name: 
            type: string
          place: 
            $ref: '#/definitions/place'

      lesson_type:
        type: object
        properties:
          id: 
            type: integer
          short_name: 
            type: string
          name: 
            type: string
      
      period:
        type: object
        properties:
          id: 
            type: integer
          short_name: 
            type: string
          name: 
            type: string

      degree:
        type: object
        properties:
          id: 
            type: integer
          name: 
            type: string

      group:
        type: object
        properties:
          id: 
            type: integer
          year: 
            type: integer
          name: 
            type: string
          degree: 
            type: string

      lesson:
        type: object
        properties:
          call: 
            $ref: '#/definitions/call'
          period: 
            $ref: '#/definitions/place'
          discipline:
            $ref: '#/definitions/discipline'
          group: 
            $ref: '#/definitions/group'
          teacher: 
            $ref: '#/definitions/teacher'
          lesson_type: 
            $ref: '#/definitions/lesson_type'
          subgroup:
            type: integer
          room:
            $ref: '#/definitions/room'
          day_of_week:
            type: integer
          week:
            type: integer

          specific_weeks:
            type: array
            items:
              type: integer
          is_usual_place: 
            type: string

          
      Day:
        type: object
        properties:
          day_num: 
            type: integer
          name: 
            type: string
          lessons: 
            type: array
            items:
              $ref: '#/definitions/Lesson'

      Week:
        type: array
        items:
          $ref: '#/definitions/Day'

      FullWeek:
        type: object
        properties:
          num:
            type: integer
          week:
            type: array
            items:
              $ref: '#/definitions/Day'

      FullSchedule:
        type: array
        items:
          $ref: '#/definitions/FullWeek'

      LessonOld:
        type: object
        nullable: true
        properties:
          lesson:
            type: object
            properties:
              classRoom: 
                type: string
              name: 
                type: string
              teacher: 
                type: string
              type: 
                type: string

          time:
            type: object
            properties:
              start: 
                type: string
              end: 
                type: string

      WeekOld: 
        type: object
        properties:
          monday:
            type: array
            items:
              $ref: '#/definitions/LessonOld'
          tuesday:
            type: array
            items:
              $ref: '#/definitions/LessonOld'
          wednesday: 
            type: array
            items:
              $ref: '#/definitions/LessonOld'
          thursday:
            type: array
            items:
              $ref: '#/definitions/LessonOld'
          friday: 
            type: array
            items:
              $ref: '#/definitions/LessonOld'
          saturday:
            type: array
            items:
              $ref: '#/definitions/LessonOld'

      FullScheduleOld:
        type: object
        nullable: true
        properties:
          first:
            $ref: '#/definitions/WeekOld'
          second:
            $ref: '#/definitions/WeekOld'


      AllWeeksOld:
        type: array
        items:
          $ref: '#/definitions/WeekOld'


      LiteDirection:
        type: object
        properties:
          name: 
            type: string
          numbers:
            type: array
            items:
              type: string

      Groups:
        type: object
        properties:
          bachelor:
            type: object
            properties:
              first:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'
              second:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'
              third:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'
              fourth:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'
          master:
            type: object
            properties:
              first:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'
              second:
                type: array
                items:
                  $ref: '#/definitions/LiteDirection'                    

    responses:
      200:
        description: Return today\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair 
        schema:
          type: array
          items:
            $ref: '#/definitions/Lesson'
          minItems: 8
          maxItems: 8

      503:
          description: Retry-After:100
    """

    sch = today_sch(group)
    if sch:
        response = jsonify(sch)
        # return "today for{} is {}".format(group, res)
        return make_response(response)
    res = Response(headers={'Retry-After': 200}, status=503)
    return res


@app.route('/api/schedule/<string:group>/tomorrow', methods=["GET"])
def tomorrow(group):
    """Tomorrow's schedule for requested group
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true

    responses:
      200:
        description: Return tomorrow\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair 
        schema:
          type: array
          items:
            $ref: '#/definitions/Lesson'
          minItems: 8
          maxItems: 8

      503:
          description: Retry-After:100
    """
    res = tomorrow_sch(group)
    if res:
        response = jsonify(res)
        # return "tomorrow for{} is {}".format(group, res)
        return make_response(response)
    res = Response(headers={'Retry-After': 200}, status=503)
    return res


@app.route('/api/schedule/<string:group>/week', methods=["GET"])
def week(group):
    """Current week's schedule for requested group
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true

    responses:
      200:
        description: Return week\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair.
        schema:
          $ref: '#/definitions/Week'

      503:
          description: Retry-After:100
    """
    res = week_sch(group)
    if res:
        response = jsonify(res)
        # return "tomorrow for{} is {}".format(group, res)
        return make_response(response)
    res = Response(headers={'Retry-After': 200}, status=503)
    return res


@app.route('/api/schedule/get_groups', methods=["GET"])
def groups():
    """List of groups in IIT
      ---
      tags:
        - OLD Groups
      responses:
        200:
          description: Return all groups in IIT.
          schema:
            $ref: '#/definitions/Groups'


        503:
            description: Retry-After:100
    """
    res = get_groups_old()
    if res:
        response = jsonify(res)

        # return "tomorrow for{} is {}".format(group, res)
        return make_response(response)
    res = Response(headers={'Retry-After': 200}, status=503)
    return res


@app.route('/api/schedule/<string:group>/next_week', methods=["GET"])
def next_week(group):
    """Next week's schedule for requested group
    ---
    tags:
      - OLD Groups
    parameters:
      - name: group
        in: path
        type: string
        required: true

    responses:
      200:
        description: Return week\'s schedule. There are 8 lessons on a day. "lesson":null, if there is no pair.
        schema:
          $ref: '#/definitions/Week'

      503:
          description: Retry-After:100
    """
    res = next_week_sch(group)
    if res:
        response = jsonify(res)
        # return "tomorrow for{} is {}".format(group, res)
        return make_response(response)
    res = Response(headers={'Retry-After': 200}, status=503)
    return res


@app.route('/api/schedule/<string:group>/full_schedule', methods=["GET"])
def full_schedule(group):
    """Current week's schedule for requested group
      ---
      tags:
        - OLD Groups
      parameters:
        - name: group
          in: path
          type: string
          required: true

      responses:
        200:
          description: Return full schedule of one group. 
          schema:
            $ref: '#/definitions/FullSchedule'

        503:
            description: Retry-After:100
    """
    sch = full_sched(group)
    if sch:
        response = jsonify(sch)
        # return "today for{} is {}".format(group, res)
        return make_response(response)
    res = Response(headers={'Retry-After': 200}, status=503)
    return res


@app.route('/api/schedule/<string:group>/<int:max_weeks>/all_weeks', methods=["GET"])
def get_all_weeks_schedule(group, max_weeks):
    """Returns all weeks up to max_weeks
      ---
      tags:
        - OLD Groups
      parameters:
        - name: group
          in: path
          type: string
          required: true
        - name: max_weeks
          in: path
          type: integer
          required: true
          description: The number of consecutive weeks returned

      responses:
        200:
          description: Return full schedule of one group. 
          schema:
            $ref: '#/definitions/AllWeeks'

        503:
            description: Retry-After:100
    """
    sch = get_full_schedule_by_weeks(group, max_weeks)
    if sch:
        response = jsonify(sch)
        return make_response(response)
    res = Response(headers={'Retry-After': 200}, status=503)
    return res


@app.route('/api/schedule/<string:group>/<int:week>/week_num', methods=["GET"])
def get_week_schedule_by_week_num(group, week):
    """Returns week schedule by week number
      ---
      tags:
        - OLD Groups
      parameters:
        - name: group
          in: path
          type: string
          required: true
        - name: week
          in: path
          type: integer
          required: true

      responses:
        200:
          description: Return full schedule of one group. 
          schema:
            $ref: '#/definitions/Week'

        503:
            description: Retry-After:100
    """
    sch = get_schedule_by_week(group, week)
    if sch:
        response = jsonify(sch)
        return make_response(response)
    res = Response(headers={'Retry-After': 200}, status=503)
    return res

# NEW ROOTS!
# --- GROUPS ---


@app.route('/api/group/', methods=["GET"])
def get_groups():
    """Returns full group schedule
      ---
      tags:
        - Group

      parameters:
        - name: institute
          in: query
          type: string
          description: "You can choose ИИТ. Please enter this parameter to make sure you get the room that you need."

      responses:
        200:
          description: Return array with days of weeks - array[0] is Monday, array[1] is Tuesday and so on. Array lenght is 6. Day is an object with key "lessons".
          schema:
            type: array
            items:
              $ref: '#/definitions/group'

        503:
            description: Retry-After:100
    """
    institute = request.args.get('institute')
    sch = get_groups_info(institute)
    if sch == 'empty':
        return Response(status=404)
    if sch:
        response = jsonify(sch)
        return make_response(response)
    res = Response(headers={'Retry-After': 200}, status=503)
    return res


@app.route('/api/lesson/', methods=["GET"])
def get_lessons():
    """Returns full group schedule
      ---
      tags:
        - Lesson

      parameters:
        - name: group
          in: query
          type: string

        - name: room
          in: query
          type: string

        - name: teacher
          in: query
          type: string

        - name: specific_week
          in: query
          type: integer

      responses:
        200:
          description: Return array with days of weeks - array[0] is Monday, array[1] is Tuesday and so on. Array lenght is 6. Day is an object with key "lessons".
          schema:
            type: array
            items:
              $ref: '#/definitions/lesson'


        503:
            description: Retry-After:100
    """
    group = request.args.get('group')
    teacher = request.args.get('teacher')
    room = request.args.get('room')
    specific_week = request.args.get('specific_week')

    if group or teacher or room:
      sch = get_lessons_list(group=group, specific_week=specific_week, teacher=teacher, room=room, week=None)
      if sch == 'empty':
          return Response(status=404)
      if sch != None:
          response = jsonify(sch)
          return make_response(response)
      res = Response(headers={'Retry-After': 200}, status=503)
      return res
    return Response(status=404)

# @app.route('/api/lesson/<int:id>/', methods=["GET"])
# def get_lesson_by_id(id):
#     """Returns group schedule by week number
#       ---
#       tags:
#         - Lesson

#       responses:
#         200:
#           description: Return array with days of weeks - array[0] is Monday, array[1] is Tuesday and so on. Array lenght is 6. Day is an object with key "lessons".
#           schema:
#             $ref: '#/definitions/lesson'

#         503:
#             description: Retry-After:100
#     """

#     sch = get_lessons(id)

#     if sch:
#         response = jsonify(sch)
#         return make_response(response)
#     res = Response(headers={'Retry-After': 200}, status=503)
#     return res


# # --- TEACHERS ---


# @app.route('/api/schedule/teachers/<string:group>/', methods=["GET"])
# def get_teacher_shedule(teacher):
#     """Returns full teacher schedule
#       ---
#       tags:
#         - Teachers

#       parameters:
#         - name: group
#           in: path
#           type: string
#           required: true

#       responses:
#         200:
#           description: Return array with days of weeks - array[0] is Monday, array[1] is Tuesday and so on. Array lenght is 6. Day is an object with key "lessons".
#           schema:
#             $ref: '#/definitions/FullTeacherSchedule'

#         503:
#             description: Retry-After:100
#     """

#     sch = get_full_sem_schedule(teacher)

#     if sch:
#         response = jsonify(sch)
#         return make_response(response)
#     res = Response(headers={'Retry-After': 200}, status=503)
#     return res


# @app.route('/api/schedule/groups/<string:group>/<int:week>/', methods=["GET"])
# def get_teacher_shedule_by_week(teacher, week):
#     """Returns teacher schedule by week number
#       ---
#       tags:
#         - Teachers

#       parameters:
#         - name: group
#           in: path
#           type: string
#           required: true
#         - name: week
#           in: path
#           type: integer
#           required: true

#       responses:
#         200:
#           description: Return array with days of weeks - array[0] is Monday, array[1] is Tuesday and so on. Array lenght is 6. Day is an object with key "lessons".
#           schema:
#             $ref: '#/definitions/Week'

#         503:
#             description: Retry-After:100
#     """

#     sch = get_sem_schedule(group, week)

#     if sch:
#         response = jsonify(sch)
#         return make_response(response)
#     res = Response(headers={'Retry-After': 200}, status=503)
#     return res

# # --- ROOMS ---


# @app.route('/api/schedule/rooms/<string:room>/<int:week>/', methods=["GET"])
# def get_room_shedule_by_week(room, week):
#     """Returns room schedule by week number
#       ---
#       tags:
#         - Rooms

#       parameters:
#         - name: room
#           in: path
#           type: string
#           required: true
#         - name: week
#           in: path
#           type: integer
#           required: true
#         - name: place
#           in: query
#           type: string
#           description: "You can choose В-78, В-86, С-20, МП-1 or СГ-22. Please enter this parameter to make sure you get the room that you need."

#       responses:
#         200:
#           description: Return array with days of weeks - array[0] is Monday, array[1] is Tuesday and so on. Array lenght is 6. Day is an object with key "lessons".
#           schema:
#             $ref: '#/definitions/Week'

#         503:
#             description: Retry-After:100
#     """
#     place = request.args.get('place')
#     sch = get_rooms_schedule_by_week(room, week, place)
#     if sch == 'empty':
#         return Response(status=404)
#     if sch:
#         response = jsonify(sch)
#         return make_response(response)
#     res = Response(headers={'Retry-After': 200}, status=503)
#     return res


# @app.route('/api/schedule/rooms/<string:room>/', methods=["GET"])
# def get_room_shedule(room):
#     """Returns room schedule by week number
#       ---
#       tags:
#         - Rooms

#       parameters:
#         - name: room
#           in: path
#           type: string
#           required: true
#         - name: place
#           in: query
#           type: string
#           description: "You can choose В-78, В-86, С-20, МП-1 or СГ-22. Please enter this parameter to make sure you get the room that you need. This is highly recommended if room name starts with 'А' or 'Б'"

#       responses:
#         200:
#           description: Return array with days of weeks - array[0] is Monday, array[1] is Tuesday and so on. Array lenght is 6. Day is an object with key "lessons".
#           schema:
#             $ref: '#/definitions/Week'

#         503:
#             description: Retry-After:100
#     """
#     place = request.args.get('place')

#     sch = get_rooms_schedule(room, place)
#     if sch == 'empty':
#         return Response(status=404)
#     if sch:
#         response = jsonify(sch)
#         return make_response(response)
#     res = Response(headers={'Retry-After': 200}, status=503)
#     return res


# @app.route('/api/schedule/rooms/', methods=["GET"])
# def get_rooms():
#     """Returns full group schedule
#       ---
#       tags:
#         - Rooms

#       parameters:
#         - name: place
#           in: query
#           type: string
#           description: "You can choose В-78, В-86, С-20, МП-1 or СГ-22. Please enter this parameter to make sure you get the room that you need. This is highly recommended if room name starts with 'А' or 'Б'"


#       responses:
#         200:
#           description: Return array with days of weeks - array[0] is Monday, array[1] is Tuesday and so on. Array lenght is 6. Day is an object with key "lessons".
#           schema:
#             type: array
#             items:
#               $ref: '#/definitions/Room'

#         503:
#             description: Retry-After:100
#     """
#     place = request.args.get('place')
#     sch = get_rooms_info(place)

#     if sch:
#         response = jsonify(sch)
#         return make_response(response)
#     res = Response(headers={'Retry-After': 200}, status=503)
#     return res

# # --- OTHER ---


@app.route('/api/current_week/', methods=["GET"])
def get_current_week():
    """Returns current week
      ---
      tags:
        - General

      responses:
        200:
          description: Return current days of week
          schema:
            $ref: '#/definitions/Week'

        503:
            description: Retry-After:100
    """
    offset = dt.timedelta(hours=3)
    time_zone = dt.timezone(offset, name='МСК')
    sch = cur_week(datetime.now(tz=time_zone))
    if sch:
        response = jsonify(sch)
        return make_response(response)
    res = Response(headers={'Retry-After': 200}, status=503)
    return res


@app.route('/refresh/', methods=["POST"])
def refresh():
    """Refresh shedule
    ---
    tags:
      - Closed
    responses:
      200:
        description: Return \'ok\' after updating
        schema:
          type: object
          properties:
            status:
              type: string
    """
    parse_schedule()
    return make_response({"status": 'ok'})


@app.route('/api/set_weeks_count/', methods=["POST"])
def set_weeks_count():
    """Refresh shedule
    ---
    tags:
      - Closed
    parameters:
      - in: body
        name: weeks_count
        required: true
        schema:
          type: object
          properties:
            value:
              type: integer

      - in: header
        name: X-Auth-Token
        type: string
        required: true

    responses:
      200:
        description: Return \'ok\' after updating
        schema:
          type: object
          properties:
            status:
              type: string
    """
    try:
        secret = request.headers.get('X-Auth-Token')
        SECRET_FOR_REFRESH = environ.get('SECRET_FOR_REFRESH')
        if secret == SECRET_FOR_REFRESH:

            weeks = request.get_json('weeks_count')["value"]
            try:
                db_weeks = WorkingData.query.filter_by(
                    name="week_count").first()
                db_weeks.value = str(weeks)
                db.session.commit()

            except Exception as err:
                week_count = get_or_create(session=db.session, model=WorkingData,
                                           name="week_count", value=str(weeks))
                db.session.commit()

            return make_response({"status": 'ok'})
        return make_response({"status": 'wrong_password'}, 401)
    except:
        return make_response({"status": 'need_password'}, 401)


@app.route('/api/secret_refresh/', methods=["POST"])
def secret_refresh():
    """Refresh shedule
    ---
    tags:
      - Closed
    parameters:
        - in: header
          name: X-Auth-Token
          type: string
          required: true

    responses:
      200:
        description: Return \'ok\' after updating
        schema:
          type: object
          properties:
            status:
              type: string
    """
    try:
        secret = request.headers.get('X-Auth-Token')
        SECRET_FOR_REFRESH = environ.get('SECRET_FOR_REFRESH')
        if secret == SECRET_FOR_REFRESH:
            parse_schedule()
            return make_response({"status": 'ok'})
        return make_response({"status": 'wrong_password'}, 401)
    except:
        return make_response({"status": 'need_password'}, 401)
