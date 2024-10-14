import out.test_pb2 as test_pb2
import out.test_pb2_grpc as test_pb2_grpc
import google.protobuf.empty_pb2 as empty

from samplebase import SampleBase

from concurrent import futures

import drawable

import grpc

currentScore = drawable.textScore()
ballsLeft = drawable.text()
gameOver = drawable.text()

class testServer(test_pb2_grpc.testGRPCServicer):
    def __init__(self):
        self.score = 0
        self.ballsLeft = 0

    def setStatus(self, request, context):
        self.score = request.score.count

        currentScore.setScore(request.score.count)
        self.updateBallsLeft(request.ballsLeft)
        return empty.Empty()
    
    def displayLaunchPower(self, request, context):
        print("current launch power set to: " + str(request.power)) 
        return empty.Empty()
    
    def showGameOver(self, request, context):
        currentScore.enable(False)
        ballsLeft.enable(False)
        gameOver.enable(True)

        return empty.Empty()

    def startGame(self, request, context):
        currentScore.enable(True)
        ballsLeft.enable(True)
        gameOver.enable(False)
        return empty.Empty()

    def updateBallsLeft(self, balls):
        if (self.ballsLeft != balls):
            self.ballsLeft = balls
            ballsLeft.setText("Balls: " + str(balls))
    
    def showHighScores(self, request, context):
        for score in request.scores:
            print(score.user.name + ":" + str(score.score.count))
        return empty.Empty()

class matrixScreen(SampleBase):
    def __init__(self, *args, **kwargs):
        super(matrixScreen, self).__init__(*args, **kwargs)

    def run(self):
        # Grpc server start
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        test_pb2_grpc.add_testGRPCServicer_to_server(testServer(), server)
        server.add_insecure_port("[::]:50051")
        server.start()
        print("---------------------------------------------")

        # Drawing logic
        screen = drawable.screen()
        screen.registerObject(currentScore)
        screen.registerObject(ballsLeft)
        screen.registerObject(gameOver)
        gameOver.setPos(24, 70)

        ballsLeft.setPos(0, 64)
        ballsLeft.setText("Balls: 3")
        gameOver.setText("Game Over")
        gameOver.enable(False)

        canvas = self.matrix.CreateFrameCanvas()

        while True:
            screen.update()
            canvas.Clear()
            screen.draw(canvas)
            canvas = self.matrix.SwapOnVSync(canvas)

if __name__ == "__main__":
    matrix = matrixScreen()
    if (not matrix.process()):
        matrixScreen.print_help()


