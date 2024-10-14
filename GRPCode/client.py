import out.test_pb2 as test_pb2
import out.test_pb2_grpc as test_pb2_grpc
import google.protobuf.empty_pb2 as empty

import grpc

channel = grpc.insecure_channel('localhost:50051')
stub = test_pb2_grpc.testGRPCStub(channel)

newStatus = test_pb2.Status()
newStatus.ballsLeft = 2
newStatus.score.count = 3


stub.setStatus(newStatus)
stub.showGameOver(empty.Empty())