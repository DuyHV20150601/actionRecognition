`threadsList=[]
	    for item in result:
			t = threading.Thread(target = workthread, args=(item, self.user_agent, self.path))
			threadsList.append(t)
			t.start()
		for threadid in threadsList:
			threadid.join() `

` # ??case_list???case
        threads = []
        for i in range(len(total_case)):
            threads.append(Thread(target=obj.run_case, args=(total_case[i], "thread_{}".format(i), result)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return self.deal_with_result(result) `


`
def data_loading(minibatch_size, data_iterator, shapeInput, exit_size):
    queue_train = Queue(maxsize=exit_size*10)
    queue_test = Queue(maxsize=exit_size*10)
    def start_loading():
        for e in range(exit_size):
            iterator_train = data_iterator(shapeInput, minibatch_size, shuffle=True, train=True)
            iterator_test = data_iterator(shapeInput, minibatch_size, shuffle=True, train=False)
            for new_input in iterator_train:
                while queue_train.full():
                    print('Queue full')
                    time.sleep(30)
                queue_train.put(new_input)
                new_input_test = iterator_test.next()
                queue_test.put(new_input_test)
        print('Exiting queue')

    t = threading.Thread(target=start_loading)
    t.daemon = True
    t.start()
    return queue_train, queue_test
`