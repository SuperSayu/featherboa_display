from neosequence import Run

# rgb values 
bhi = [75,50,125]
blo = [25,0,75]
rhi = [125,75,50]
rlo = [75,25,0]
ghi = [50,125,75]
glo = [0,75,25]
off = [0,0,0]

# Syntactic sugar
state = lambda rgb,t: rgb + [t,20]
hlho = lambda hi,lo: [state(hi,2.3),state(lo,0.7),state(hi,2.45),state(off,0)] # high, low, high, off

# Run(Sequence_List)
#   Sequence_List: [State_List,State_list,...]
#     State_List: [State,State,...]
#       State: [r,g,b, hold_time_in_seconds, step_count]
# Note that step_count is how many colors it goes through leading in to the state, not leading out of it.
Run([
  hlho(bhi,blo) + hlho(rhi,rlo) + hlho(ghi,glo),
  hlho(rhi,rlo),
  hlho(bhi,blo),
  hlho(ghi,glo)
  ])