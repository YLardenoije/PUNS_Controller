import out.test_pb2 as test_pb2
import out.test_pb2_grpc as test_pb2_grpc
import google.protobuf.empty_pb2 as empty

from concurrent import futures

import grpc

class testServer(test_pb2_grpc.testGRPCServicer):
    def __init__(self):
        self.score = 0
        self.ballsLeft = 0

    def setStatus(self, request, context):
        self.score = request.score.count
        if (self.ballsLeft != request.ballsLeft):
            self.ballsLeft = request.ballsLeft
            print("Balls left: " + str(self.ballsLeft))
        return empty.Empty()
    
    def displayLaunchPower(self, request, context):
        print("current launch power set to: " + str(request.power)) 
        return empty.Empty()
    
    def showGameOver(self, request, context):
        print("You lost!")
        print("Your finishing score:")
        print(self.score)

        self.score = 0
        self.ballsLeft = 0

        return empty.Empty()
    
    def showHighScores(self, request, context):
        for score in request.scores:
            print(score.user.name + ":" + str(score.score.count))
        return empty.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    test_pb2_grpc.add_testGRPCServicer_to_server(testServer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

serve()